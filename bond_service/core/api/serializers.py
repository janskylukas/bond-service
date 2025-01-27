from datetime import datetime

import requests
from django.utils import timezone
from rest_framework import serializers
from rest_framework import status
from stdnum import isin

from bond_service.core.api.exceptions import InvalidISINError
from bond_service.core.models import Bond


class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = "__all__"
        read_only_fields = ["owner"]

    def validate_isin(self, value) -> str:
        if not isin.is_valid(value):
            raise InvalidISINError(value)

        response = requests.get(
            # This might be in the settings file, but since we use it only once,
            # I kept it here
            f"https://www.cdcp.cz/isbpublicjson/api/VydaneISINy?isin={value}",
            headers={"Accept": "application/json"},
            timeout=10,
        )
        if response.status_code != status.HTTP_200_OK:
            raise InvalidISINError(value)

        if not response.json().get(
            "vydaneisiny",
        ):
            raise InvalidISINError(value)

        return value

    def validate_maturity_date(self, value):
        purchase_date = (
            datetime.strptime(
                self.initial_data["purchase_date"],
                "%Y-%m-%d",
            )
            .astimezone(timezone.get_current_timezone())
            .date()
        )

        if value < purchase_date:
            msg = "Maturity date must be after purchase date."
            raise serializers.ValidationError(msg)
        return value
