import pytest
from users.models import AbstractUser
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


User = get_user_model()
UData = dict[str, str]

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
    def test_registration_success(
        self,
        client: APIClient,
        user_data: UData,
    ):
        """Successful registration returns tokens."""
        url = reverse('users:register')
        response = client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'accessToken' in response.data
        assert 'refreshToken' in response.cookies

    def test_registration_creates_user_in_db(
        self,
        client: APIClient,
        user_data: UData,
    ):
        """Successful registration creates a user in database."""
        url = reverse('users:register')
        client.post(url, user_data, format='json')

        assert User.objects.filter(username='testuser').exists()

    def test_registration_duplicate_username(
        self,
        client: APIClient,
        user_data: UData,
        existing_user: AbstractUser,
    ):
        """Registration with existing username returns validation error."""
        url = reverse('users:register')
        user_data['username'] = existing_user.username

        response = client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(
        'field, value',
        [
            ('username', ''),
            ('password', ''),
        ],
    )
    def test_registration_empty_required_fields(
        self,
        client: APIClient,
        user_data: UData,
        field: str,
        value: str,
    ):
        """Empty required fields return validation error."""
        url = reverse('users:register')
        user_data[field] = value

        response = client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_passwords_mismatch(
        self,
        client: APIClient,
        user_data: UData,
    ):
        """Different passwords return validation error."""
        url = reverse('users:register')
        user_data['password2'] = 'DifferentPass456!'

        response = client.post(url, user_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_sets_refresh_cookie_httponly(
        self,
        client: APIClient,
        user_data: UData,
    ):
        """Registration sets httponly refresh token cookie."""
        url = reverse('users:register')

        response = client.post(url, user_data, format='json')

        cookie = response.cookies.get('refreshToken')

        assert cookie is not None
        assert cookie['httponly']
