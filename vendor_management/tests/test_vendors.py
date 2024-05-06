from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest


# Tests for POST request on /api/vendors/ endpoint.
@pytest.mark.django_db
class TestCreateVendor:
    def test_authenticated_user_return_201(self):
        # Act
        user = User.objects.create_user(username='testuser', password='1234')

        # Authenticate the user
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post('/api/vendors/', {
            "name": "a",
            "contact_details": "9",
            "address": "b"
        })
        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_authenticated_user_return_400(self):
        # Act
        user = User.objects.create_user(username='testuser', password='1234')

        # Authenticate the user
        client = APIClient()
        client.force_authenticate(user=user)

        response = client.post('/api/vendors/', {
            "name": "a",
            "contact_details": "9"
        })
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anonymous_user_return_401(self):
        # Act
        client = APIClient()
        response = client.post('/api/vendors/', {
            "name": "a",
            "contact_details": "9",
            "address": "b"
        })
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
