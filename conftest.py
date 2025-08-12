import pytest
import requests
import uuid
import logging
from data.handlers import Handlers
from data.user_data import User

logger = logging.getLogger(__name__)

@pytest.fixture
def create_user():
    """
    Фикстура для создания, авторизации и последующего удаления тестового пользователя.
    Возвращает:
    - token (str): Токен авторизации пользователя
    """
    # 1. Подготовка уникальных данных пользователя
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "email": unique_email,
        "password": User.DEFAULT_PASSWORD,
        "name": User.DEFAULT_NAME
    }

    # 2. Регистрация пользователя
    try:
        register_response = requests.post(
            Handlers.full_url(Handlers.CREATE_USER),
            headers=Handlers.HEADERS_JSON,
            json=user_data,
            timeout=10
        )
        register_response.raise_for_status()
        logger.info(f"Пользователь создан: {unique_email}")
    except Exception as e:
        logger.error(f"Ошибка регистрации пользователя: {str(e)}")
        pytest.fail(f"Не удалось зарегистрировать пользователя: {str(e)}")

    # 3. Авторизация пользователя
    try:
        login_response = requests.post(
            Handlers.full_url(Handlers.LOGIN),
            headers=Handlers.HEADERS_JSON,
            json={"email": unique_email, "password": User.DEFAULT_PASSWORD},
            timeout=10
        )
        login_response.raise_for_status()
        token = login_response.json().get("accessToken")
        if not token:
            raise ValueError("Токен авторизации не получен")
        logger.info(f"Пользователь авторизован: {unique_email}")
    except Exception as e:
        logger.error(f"Ошибка авторизации: {str(e)}")
        pytest.fail(f"Не удалось авторизовать пользователя: {str(e)}")

    # 4. Передача токена в тест
    yield token

    # 5. Удаление пользователя (пост-очистка)
    try:
        delete_response = requests.delete(
            Handlers.full_url(Handlers.DELETE_USER),
            headers=Handlers.auth_headers(token),
            timeout=10
        )
        if delete_response.status_code != 202:
            raise ValueError(f"Неожиданный статус код: {delete_response.status_code}")
        logger.info(f"Пользователь удалён: {unique_email}")
    except Exception as e:
        logger.error(f"Ошибка удаления пользователя: {str(e)}")
        # Не вызываем pytest.fail() в финализаторе, чтобы не влиять на результат теста






