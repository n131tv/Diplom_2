import pytest
import requests
import uuid
import logging
import allure
from data.handlers import Urls, Handlers

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


@pytest.fixture(scope="function")
def create_user():
    """
    Фикстура для создания тестового пользователя перед тестом
    и его удаления после завершения теста.
    Возвращает accessToken созданного пользователя.
    """
    # Генерация уникального email
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "Test1234!",
        "name": "Test User"
    }

    # Создание пользователя
    with allure.step("Создание тестового пользователя"):
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.CREATE_USER}",
            json=payload,
            timeout=10
        )

        logger.info(f"Создание пользователя: статус {response.status_code}")
        assert response.status_code == 200, "Не удалось создать пользователя"
        token = response.json().get("accessToken")
        assert token is not None, "Токен не получен"

    yield token  # Передаем токен в тест

    # Удаление пользователя после теста
    with allure.step("Удаление тестового пользователя"):
        headers = {"Authorization": token}
        delete_response = requests.delete(
            f"{Urls.MAIN_URL}{Handlers.DELETE_USER}",
            headers=headers,
            timeout=10
        )

        logger.info(f"Удаление пользователя: статус {delete_response.status_code}")
        if delete_response.status_code != 200:
            logger.error(f"Ошибка при удалении пользователя: {delete_response.text}")








