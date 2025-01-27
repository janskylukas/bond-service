import factory
from django.contrib.auth.models import User

from bond_service.core.models import Bond


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence("user{0}".format)
    password = factory.PostGenerationMethodCall("set_password", "password")


class BondFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bond

    name = factory.Sequence("bond{0}".format)
    isin = factory.Sequence("CZ{0}".format)
    value = factory.Sequence(lambda n: (n + 1) * 1000.0)
    interest_rate = factory.Sequence(lambda n: (n + 1) * 0.5)
    purchase_date = factory.Sequence(lambda n: f"2022-01-{n + 1:02d}")
    maturity_date = factory.Sequence(lambda n: f"2025-01-{n + 1:02d}")
    owner = factory.SubFactory(UserFactory)
