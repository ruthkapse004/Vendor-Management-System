from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


# Tests for GET request on /api/purchase_orders/ & /api/purchase_orders/po_number endpoint.
@pytest.mark.django_db
class TestGetPurchaseOrderAPI:
    # Tests for Listing Purchase Order
    def test_authenticated_user_get_200(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='1234')
        client.force_authenticate(user=user)

        # Act
        response = client.get('/api/purchase_orders/')

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_anonymous_user_get_401(self):
        # Arrange
        client = APIClient()

        # Act
        response = client.get('/api/purchase_orders/')

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Tests for Retrieving Purchase Order Using po_number
    def test_anonymous_user_retrieve_401(self):
        # Arrange
        client = APIClient()
        po_number = "1714988795719214"

        # Act
        response = client.get('/api/purchase_orders/po_number/',
                              {'po_number': po_number})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_retrieve_404(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='1234')
        client.force_authenticate(user=user)

        # Act
        response = client.get('/api/purchase_orders/po_number/',
                              {'po_number': 'invalid-po-number'})

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


# Tests for POST request on /api/purchase_orders/ endpoint.
@ pytest.mark.django_db
class TestPostPurchaseOrderAPI:
    def test_authenticated_user_post_400(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='1234')
        client.force_authenticate(user=user)

        # Act
        response = client.post('/api/purchase_orders/', {
            "vendor": 1,
            "delivery_date": "2024-05-06",
            "quantity": 2,
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anonymous_user_post_401(self):
        # Arrange
        client = APIClient()

        # Act
        response = client.post('/api/purchase_orders/', {
            "vendor": 1,
            "delivery_date": "2024-05-06",
            "quantity": 2,
        })

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
