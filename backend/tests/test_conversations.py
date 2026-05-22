import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import Conversation, Message
from companion.models import Companion
from django.utils import timezone
import uuid

User = get_user_model()


# ===========================
# ФИКСТУРЫ
# ===========================

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        password='StrongPass123!'
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username='otheruser',
        password='StrongPass123!'
    )


@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def companion(db, user):
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
def other_companion(db, other_user):
    return Companion.objects.create(
        name='Stranger',
        avatar='avatar_2',
        owner_id=other_user,
        birth_date=timezone.now(),
        gender='female',
        eye_color='blue',
        hair_color='black',
    )


@pytest.fixture
def conversation(db, user, companion):
    return Conversation.objects.create(
        title=companion.name,
        user_id=user,
        companion_id=companion,
    )


@pytest.fixture
def message(db, conversation):
    return Message.objects.create(
        content='Hello!',
        sender_type='user',
        conversation_id=conversation,
    )


# ===========================
# ТЕСТЫ СПИСКА РАЗГОВОРОВ
# ===========================

@pytest.mark.django_db
class TestConversationListView:

    def test_get_conversations_success(self, auth_client, conversation):
        """Авторизованный пользователь получает список своих разговоров"""
        url = reverse('conversations:conversation_list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_conversations_empty(self, auth_client):
        """Нет разговоров — пустой список"""
        url = reverse('conversations:conversation_list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_conversations_unauthorized(self, client):
        """Неавторизованный пользователь не получает список"""
        url = reverse('conversations:conversation_list')
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_conversations_only_own(self, auth_client, other_user, other_companion, db):
        """Пользователь видит только свои разговоры"""
        Conversation.objects.create(
            title='Stranger chat',
            user_id=other_user,
            companion_id=other_companion,
        )

        url = reverse('conversations:conversation_list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    # --- POST ---

    def test_create_conversation_success(self, auth_client, companion):
        """Happy path — успешное создание разговора"""
        url = reverse('conversations:conversation_list')
        response = auth_client.post(url, {
            'companion_id': companion.id
        }, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Conversation.objects.filter(companion_id=companion).exists()

    def test_create_conversation_missing_companion_id(self, auth_client):
        """Не передан companion_id — ошибка 400"""
        url = reverse('conversations:conversation_list')
        response = auth_client.post(url, {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_conversation_nonexistent_companion(self, auth_client):
        """Несуществующий companion_id — 404"""
        url = reverse('conversations:conversation_list')
        response = auth_client.post(url, {
            'companion_id': 99999
        }, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_conversation_other_users_companion(self, auth_client, other_companion):
        """Нельзя создать разговор с чужим компаньоном"""
        url = reverse('conversations:conversation_list')
        response = auth_client.post(url, {
            'companion_id': other_companion.id
        }, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_conversation_duplicate(self, auth_client, companion, conversation):
        """Нельзя создать второй разговор с тем же компаньоном"""
        url = reverse('conversations:conversation_list')
        response = auth_client.post(url, {
            'companion_id': companion.id
        }, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_conversation_limit_reached(self, auth_client, user, db):
        """Нельзя создать больше 2 разговоров"""
        for i in range(2):
            companion = Companion.objects.create(
                name=f'Companion{i}',
                avatar=f'avatar_{i}',
                owner_id=user,
                birth_date=timezone.now(),
                gender='female',
                eye_color='brown',
                hair_color='brown',
            )
            Conversation.objects.create(
                title=f'Chat{i}',
                user_id=user,
                companion_id=companion,
            )

        # Третий компаньон
        third_companion = Companion.objects.create(
            name='Third',
            avatar='avatar_3',
            owner_id=user,
            birth_date=timezone.now(),
            gender='female',
            eye_color='brown',
            hair_color='brown',
        )

        url = reverse('conversations:conversation_list')
        response = auth_client.post(url, {
            'companion_id': third_companion.id
        }, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_conversation_unauthorized(self, client, companion):
        """Неавторизованный пользователь не может создать разговор"""
        url = reverse('conversations:conversation_list')
        response = client.post(url, {
            'companion_id': companion.id
        }, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ===========================
# ТЕСТЫ ДЕТАЛЬНОГО ПРОСМОТРА
# ===========================

@pytest.mark.django_db
class TestConversationDetailView:

    def test_get_conversation_success(self, auth_client, conversation):
        """Успешное получение разговора по id"""
        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': conversation.id
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_conversation_not_found(self, auth_client):
        """
        Несуществующий id.
        """
        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': uuid.uuid4()
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_conversation_of_other_user(self, auth_client, other_user, other_companion, db):
        """
        Запрос чужого разговора.
        """
        other_conversation = Conversation.objects.create(
            title='Stranger chat',
            user_id=other_user,
            companion_id=other_companion,
        )

        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': other_conversation.id
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_conversation_unauthorized(self, client, conversation):
        """Неавторизованный пользователь не получает разговор"""
        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': conversation.id
        })
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # --- DELETE ---

    def test_delete_conversation_success(self, auth_client, conversation):
        """Успешное удаление разговора"""
        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': conversation.id
        })
        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Conversation.objects.filter(id=conversation.id).exists()

    def test_delete_conversation_not_found(self, auth_client):
        """Несуществующий разговор — 404"""
        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': uuid.uuid4()
        })
        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_conversation_of_other_user(self, auth_client, other_user, other_companion, db):
        """Нельзя удалить чужой разговор"""
        other_conversation = Conversation.objects.create(
            title='Stranger chat',
            user_id=other_user,
            companion_id=other_companion,
        )

        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': other_conversation.id
        })
        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Conversation.objects.filter(id=other_conversation.id).exists()

    def test_delete_conversation_unauthorized(self, client, conversation):
        """Неавторизованный пользователь не может удалить разговор"""
        url = reverse('conversations:conversation_detail', kwargs={
            'conversation_id': conversation.id
        })
        response = client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Conversation.objects.filter(id=conversation.id).exists()


# ===========================
# ТЕСТЫ СООБЩЕНИЙ
# ===========================

@pytest.mark.django_db
class TestMessageListView:

    def test_get_messages_success(self, auth_client, conversation, message):
        """Успешное получение списка сообщений"""
        url = reverse('conversations:message_list', kwargs={
            'conversation_id': conversation.id
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['content'] == 'Hello!'

    def test_get_messages_empty(self, auth_client, conversation):
        """Нет сообщений — пустой список"""
        url = reverse('conversations:message_list', kwargs={
            'conversation_id': conversation.id
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_messages_unauthorized(self, client, conversation):
        """Неавторизованный пользователь не получает сообщения"""
        url = reverse('conversations:message_list', kwargs={
            'conversation_id': conversation.id
        })
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_messages_of_other_user(self, auth_client, other_user, other_companion, db):
        """Нельзя получить сообщения чужого разговора"""
        other_conversation = Conversation.objects.create(
            title='Stranger chat',
            user_id=other_user,
            companion_id=other_companion,
        )
        Message.objects.create(
            content='Secret message',
            sender_type='user',
            conversation_id=other_conversation,
        )

        url = reverse('conversations:message_list', kwargs={
            'conversation_id': other_conversation.id
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0


# ===========================
# ТЕСТЫ ДЕТАЛЬНОГО СООБЩЕНИЯ
# ===========================

@pytest.mark.django_db
class TestMessageDetailView:

    def test_get_message_success(self, auth_client, conversation, message):
        """Успешное получение сообщения по id"""
        url = reverse('conversations:message_detail', kwargs={
            'conversation_id': conversation.id,
            'message_id': message.id,
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == 'Hello!'

    def test_get_message_not_found(self, auth_client, conversation):
        """
        БАГ: MessageDetailView.get() не имеет try/except.
        Несуществующее сообщение даёт 500 вместо 404.
        """
        url = reverse('conversations:message_detail', kwargs={
            'conversation_id': conversation.id,
            'message_id': 99999,
        })
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_message_unauthorized(self, client, conversation, message):
        """Неавторизованный пользователь не получает сообщение"""
        url = reverse('conversations:message_detail', kwargs={
            'conversation_id': conversation.id,
            'message_id': message.id,
        })
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
