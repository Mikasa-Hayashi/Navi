import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from companion.models import Companion
from django.utils import timezone

User = get_user_model()


# ===========================
# ФИКСТУРЫ
# ===========================

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    """Авторизованный пользователь"""
    return User.objects.create_user(
        username='testuser',
        password='StrongPass123!'
    )


@pytest.fixture
def other_user(db):
    """Другой пользователь — для проверки изоляции данных"""
    return User.objects.create_user(
        username='otheruser',
        password='StrongPass123!'
    )


@pytest.fixture
def auth_client(client, user):
    """Клиент с авторизованным пользователем"""
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def companion(db, user):
    """Готовый компаньон в БД"""
    return Companion.objects.create(
        name='Aria',
        avatar='avatar_1',
        owner_id=user,
        birth_date=timezone.now(),
        gender='female',
        eye_color='brown',
        hair_color='brown',
    )


@pytest.fixture
def companion_data():
    """Валидные данные для создания компаньона"""
    return {
        'name': 'Luna',
        'avatar': 'avatar_2',
    }


# ===========================
# ТЕСТЫ СПИСКА КОМПАНЬОНОВ
# ===========================

@pytest.mark.django_db
class TestCompanionListView:

    def test_get_companions_success(self, auth_client, companion):
        """Авторизованный пользователь получает список своих компаньонов"""
        url = reverse('companions:companion_list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Aria'

    def test_get_companions_empty(self, auth_client):
        """Нет компаньонов — возвращается пустой список"""
        url = reverse('companions:companion_list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_companions_unauthorized(self, client):
        """Неавторизованный пользователь не получает список"""
        url = reverse('companions:companion_list')
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_companions_only_own(self, auth_client, user, other_user, db):
        """Пользователь видит только своих компаньонов, не чужих"""
        # Компаньон другого пользователя
        Companion.objects.create(
            name='StrangerCompanion',
            avatar='avatar_3',
            owner_id=other_user,
            birth_date=timezone.now(),
            gender='female',
            eye_color='blue',
            hair_color='black',
        )

        url = reverse('companions:companion_list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    # --- POST ---

    def test_create_companion_success(self, auth_client, companion_data):
        """Happy path — успешное создание компаньона"""
        url = reverse('companions:companion_list')
        response = auth_client.post(url, companion_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Luna'
        assert Companion.objects.filter(name='Luna').exists()

    def test_create_companion_missing_name(self, auth_client, companion_data):
        """Не передано имя — ошибка 400"""
        url = reverse('companions:companion_list')
        companion_data['name'] = ''
        response = auth_client.post(url, companion_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_companion_missing_avatar(self, auth_client, companion_data):
        """Не передан аватар — ошибка 400"""
        url = reverse('companions:companion_list')
        companion_data['avatar'] = ''
        response = auth_client.post(url, companion_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_companion_missing_both(self, auth_client):
        """Не передано ни имя ни аватар — ошибка 400"""
        url = reverse('companions:companion_list')
        response = auth_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_companion_limit_reached(self, auth_client, user, db):
        """Нельзя создать больше 2 компаньонов"""
        for i in range(2):
            Companion.objects.create(
                name=f'Companion{i}',
                avatar=f'avatar_{i}',
                owner_id=user,
                birth_date=timezone.now(),
                gender='female',
                eye_color='brown',
                hair_color='brown',
            )

        url = reverse('companions:companion_list')
        response = auth_client.post(url, {
            'name': 'Third',
            'avatar': 'avatar_3'
        }, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_companion_unauthorized(self, client, companion_data):
        """Неавторизованный пользователь не может создать компаньона"""
        url = reverse('companions:companion_list')
        response = client.post(url, companion_data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_companion_name_whitespace_only(self, auth_client):
        """Имя из пробелов — ошибка 400"""
        url = reverse('companions:companion_list')
        response = auth_client.post(url, {
            'name': '   ',
            'avatar': 'avatar_1'
        }, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ===========================
# ТЕСТЫ ДЕТАЛЬНОГО ПРОСМОТРА
# ===========================

@pytest.mark.django_db
class TestCompanionDetailView:

    def test_get_companion_success(self, auth_client, companion):
        """Успешное получение компаньона по id"""
        url = reverse('companions:companion_detail', kwargs={'companion_id': companion.id})
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Aria'

    def test_get_companion_not_found(self, auth_client):
        """Несуществующий компаньон — ошибка"""
        url = reverse('companions:companion_detail', kwargs={'companion_id': 99999})
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_companion_of_other_user(self, auth_client, other_user, db):
        """Нельзя получить компаньона другого пользователя"""
        other_companion = Companion.objects.create(
            name='StrangerCompanion',
            avatar='avatar_3',
            owner_id=other_user,
            birth_date=timezone.now(),
            gender='female',
            eye_color='blue',
            hair_color='black',
        )

        url = reverse('companions:companion_detail', kwargs={'companion_id': other_companion.id})
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_companion_unauthorized(self, client, companion):
        """Неавторизованный пользователь не получает компаньона"""
        url = reverse('companions:companion_detail', kwargs={'companion_id': companion.id})
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # --- DELETE ---

    def test_delete_companion_success(self, auth_client, companion):
        """Успешное удаление компаньона"""
        url = reverse('companions:companion_detail', kwargs={'companion_id': companion.id})
        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Companion.objects.filter(id=companion.id).exists()

    def test_delete_companion_not_found(self, auth_client):
        """Удаление несуществующего компаньона — 404"""
        url = reverse('companions:companion_detail', kwargs={'companion_id': 99999})
        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_companion_of_other_user(self, auth_client, other_user, db):
        """Нельзя удалить компаньона другого пользователя"""
        other_companion = Companion.objects.create(
            name='StrangerCompanion',
            avatar='avatar_3',
            owner_id=other_user,
            birth_date=timezone.now(),
            gender='female',
            eye_color='blue',
            hair_color='black',
        )

        url = reverse('companions:companion_detail', kwargs={'companion_id': other_companion.id})
        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # Убеждаемся что чужой компаньон не удалён
        assert Companion.objects.filter(id=other_companion.id).exists()

    def test_delete_companion_unauthorized(self, client, companion):
        """Неавторизованный пользователь не может удалить компаньона"""
        url = reverse('companions:companion_detail', kwargs={'companion_id': companion.id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Companion.objects.filter(id=companion.id).exists()
