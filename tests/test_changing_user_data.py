import allure
import requests
import uuid
import logging
import pytest
from data.handlers import Urls, Handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


@pytest.fixture(scope="function")
def create_user():
    """Фикстура для создания и последующего удаления тестового пользователя"""
    # Генерация уникальных данных
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

        user_data = {
            "email": unique_email,
            "token": token
        }

    yield token  # Передаем токен тесту

    # Удаление пользователя после теста
    with allure.step("Удаление тестового пользователя"):
        headers = {"Authorization": token}
        delete_response = requests.delete(
            f"{Urls.MAIN_URL}{Handlers.DELETE_USER}",
            headers=headers,
            timeout=10
        )

        logger.info(f"Удаление пользователя: статус {delete_response.status_code}")
        if delete_response.status_code != 200:  # Проверяем ожидаемый код ответа
            logger.error(f"Ошибка при удалении пользователя: {delete_response.text}")


@allure.suite('Изменение данных пользователя')
class TestChangingUserData:

    @allure.title("Успешное изменение email авторизованного пользователя")
    def test_changing_user_email_with_auth(self, create_user):
        """Тест изменения email с проверкой корректности обновления данных"""
        # Генерация нового email
        new_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        payload = {"email": new_email}
        headers = {"Authorization": create_user}

        with allure.step("Отправка запроса на изменение email"):
            response = requests.patch(
                f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
                headers=headers,
                json=payload,
                timeout=10
            )

            logger.info(f"Статус ответа: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")

        with allure.step("Проверка результатов"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
            assert response.json()["user"]["email"] == new_email, "Email не соответствует ожидаемому значению"



