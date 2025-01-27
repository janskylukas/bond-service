from http import HTTPMethod

from django.contrib.auth.models import AnonymousUser
from django.db.models import Avg
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bond_service.core.api.serializers import BondSerializer
from bond_service.core.models import Bond


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer

    def perform_create(self, serializer):
        if isinstance(self.request.user, AnonymousUser):
            return  # This is purely for mypy, AnonymousUser would never reach there.
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return (
                None  # This is purely for mypy, AnonymousUser would never reach there.
            )
        return self.queryset.filter(owner=self.request.user)

    @action(detail=False, methods=[HTTPMethod.GET], url_path="portfolio-analysis")
    def portfolio_analysis(self, request):
        """
        Provides a portfolio analysis for the authenticated user, including
        total bond value, average interest rate, nearest maturity bond, and
        a future value calculation.

        It computes future value as:

            FV = PV * (1 + r)^n

        where:
            FV = future value
            PV = present value
            r = interest rate
            n = number of periods

        """

        bonds = self.get_queryset()

        if not bonds.exists():
            # This might even return a dict with 0 values.
            return Response({"error": "No bonds in portfolio."}, status=400)

        total_value = bonds.aggregate(Sum("value"))["value__sum"]

        avg_interest_rate = bonds.aggregate(Avg("interest_rate"))["interest_rate__avg"]

        nearest_maturity_bond = BondSerializer(
            bonds.order_by("maturity_date").first(),
            many=False,
        ).data

        future_value = sum(bond.future_value for bond in bonds)

        # The dict might be a Pydantic model to validate and type all values,
        # but due to simplicity, it is left as simple dict.
        return Response(
            {
                "total_value": total_value,
                "average_interest_rate": avg_interest_rate,
                "nearest_maturity_bond": nearest_maturity_bond,
                "future_value": future_value,
            },
        )
