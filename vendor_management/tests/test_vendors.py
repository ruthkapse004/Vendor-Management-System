from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import pytest
from vendor_management.models import Vendor


# Tests for GET request on /api/vendors/ & /api/vendors/vendor_code endpoint.
@pytest.mark.django_db
class TestGetVendorAPI:
    # Tests for Listing Vendors
    def test_authenticated_user_get_200(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='1234')
        client.force_authenticate(user=user)

        # Act
        response = client.get('/api/vendors/')

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_anonymous_user_get_401(self):
        # Arrange
        client = APIClient()

        # Act
        response = client.get('/api/vendors/')

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_user_retrieve_401(self):
        # Arrange
        client = APIClient()
        vendor_code = "5b90994e-e933-4cd6-8237-1ec70fbf3213"

        # Act
        response = client.get('/api/vendors/vendor_code/',
                              {'vendor_code': vendor_code})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_user_retrieve_404(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='1234')
        client.force_authenticate(user=user)

        # Act
        response = client.get('/api/vendors/vendor_code/',
                              {'vendor_code': 'invalid-vendor-code'})

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

# Tests for DELETE request on /api/vendors/vendor_code endpoint.


@pytest.mark.django_db
class TestDeleteVendorAPI:
    def test_authenticated_user_delete_404(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        client.force_authenticate(user=user)

        # Act
        response = client.delete(
            '/api/vendors/vendor_code/', {'vendor_code': 'invalid-vendor-code'})

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND


# Tests for POST request on /api/vendors/ endpoint.
@ pytest.mark.django_db
class TestPostVendorAPI:
    def test_authenticated_user_post_201(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='1234')
        client.force_authenticate(user=user)

        # Act
        response = client.post('/api/vendors/', {
            "name": "a",
            "contact_details": "9",
            "address": "b"
        })

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_authenticated_user_post_400(self):
        # Arrange
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='1234')
        client.force_authenticate(user=user)

        # Act
        response = client.post('/api/vendors/', {
            "name": "a",
            "contact_details": "9"
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anonymous_user_post_401(self):
        # Arrange
        client = APIClient()

        # Act
        response = client.post('/api/vendors/', {
            "name": "a",
            "contact_details": "9",
            "address": "b"
        })

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
