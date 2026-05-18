import pytest
from users.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


User = get_user_model()

# Fixtures
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'StrongPassword123!',
        'password2': 'StrongPassword123!',
    }


@pytest.fixture
def existing_user(db):
    return User.objects.create_user(
        username='existing_user',
        password='StrongPassword123!'
    )


@pytest.mark.django_db
class TestRegistrationView:
    def test_registration_success(self, client : APIClient, user_data : dict[str, str]):
        """Success registration"""
        url = reverse('users:register')
        response = client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'accessToken' in response.data
        assert 'refreshToken' in response.cookies
    
    def test_registation_creates_user_in_db(self, client : APIClient, user_data : dict[str, str]):
        """After registration user appends to db"""
        url = reverse('users:register')
        client.post(url, user_data, format='json')

        assert User.objects.filter(username='testuser').exists()
    
    def test_registration_duplicate_username(self, client : APIClient, user_data : dict[str, str], existing_user : AbstractUser):
        """Can't registrate with taken username"""
        url = reverse('users:register')
        user_data['username'] = existing_user.username
        response = client.post(url, user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
