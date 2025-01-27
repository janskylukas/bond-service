# ruff: noqa: PLR2004
from decimal import Decimal

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from bond_service.core.api.factories import BondFactory
from bond_service.core.api.factories import UserFactory
from bond_service.core.models import Bond


@pytest.mark.django_db
class TestBondAPI:
    def test_create_bond(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            "name": "Test Bond",
            "isin": "CZ0000705751",
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2022-01-01",
            "maturity_date": "2025-01-01",
            "payment_frequency": 1,
        }
        response = client.post("/api/bonds/", data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Bond.objects.count() == 1

    def test_list_bonds(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        BondFactory.create_batch(5, owner=user)
        response = client.get("/api/bonds/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_retrieve_bond(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        bond = BondFactory(owner=user)
        response = client.get(f"/api/bonds/{bond.pk}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == bond.name

    def test_update_bond(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        bond = BondFactory(owner=user)
        data = {
            "name": "Updated Bond",
            "isin": "CZ1008000047",
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2022-01-01",
            "maturity_date": "2025-01-01",
            "payment_frequency": 1,
            "owner": user.pk,
        }
        response = client.put(f"/api/bonds/{bond.pk}/", data)
        assert response.status_code == status.HTTP_200_OK
        assert Bond.objects.get(pk=bond.pk).name == "Updated Bond"

    def test_delete_bond(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        bond = BondFactory(owner=user)
        response = client.delete(f"/api/bonds/{bond.pk}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Bond.objects.count() == 0

    def test_portfolio_analysis(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        BondFactory(
            value=1000,
            interest_rate=5,
            maturity_date="2025-01-01",
            purchase_date="2022-01-01",
            payment_frequency=1,
            owner=user,
        )
        BondFactory(
            value=2000,
            interest_rate=7,
            maturity_date="2025-01-02",
            purchase_date="2022-01-02",
            payment_frequency=12,
            owner=user,
        )
        response = client.get("/api/bonds/portfolio-analysis/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["total_value"] == 3000
        assert response.data["average_interest_rate"] == 6
        assert response.data["nearest_maturity_bond"]["maturity_date"] == "2025-01-01"
        assert response.data["future_value"] == round(Decimal(8241.91), 2)


@pytest.mark.django_db
class TestBondAPIErrors:
    def test_create_bond_without_authentication(self):
        client = APIClient()
        data = {
            "name": "Test Bond",
            "isin": "CZ0000705751",
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2022-01-01",
            "maturity_date": "2025-01-01",
        }
        response = client.post("/api/bonds/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_bond_with_invalid_data(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            "name": "",  # invalid name
            "isin": "US1234567890",  # invalid ISIN
            "value": -1000.0,
            "interest_rate": -0.1,
            "purchase_date": "2022-01-01",
            "maturity_date": "2025-01-01",
        }
        response = client.post("/api/bonds/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_bond_with_missing_field(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            "name": "Test Bond",
            "isin": "US1234567890",
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2022-01-01",
        }  # missing maturity_date field
        response = client.post("/api/bonds/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_bond_without_authentication(self):
        bond = BondFactory()
        client = APIClient()
        data = {
            "name": "Updated Bond",
            "isin": "US1234567890",
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2022-01-01",
            "maturity_date": "2025-01-01",
        }
        response = client.put(f"/api/bonds/{bond.pk}/", data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_bond_with_invalid_data(self):
        user = UserFactory()
        bond = BondFactory(owner=user)
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            "name": "",  # invalid name
            "isin": "US1234567890",  # invalid ISIN
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2022-01-01",
            "maturity_date": "2025-01-01",
        }
        response = client.put(f"/api/bonds/{bond.pk}/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_bond_without_authentication(self):
        bond = BondFactory()
        client = APIClient()
        response = client.delete(f"/api/bonds/{bond.pk}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_bond_with_invalid_data(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            "name": "",  # invalid name
            "isin": "US1234567890",  # invalid ISIN
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2022-01-01",
            "maturity_date": "2025-01-01",
        }
        response = client.put("/api/bonds/1/", data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_maturity_date_before_purchase_date(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)
        data = {
            "name": "Test Bond",
            "isin": "CZ0000705751",
            "value": 1000.0,
            "interest_rate": 5.0,
            "purchase_date": "2025-01-01",
            "maturity_date": "2022-01-01",
        }
        response = client.post("/api/bonds/", data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
