import pytest
import allure
import requests
import logging

from data.handlers import Urls, Handlers
from data.user_data import User

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@allure.suite('Создание пользователя')
class TestCreateUser:

    @allure.title('Создание нового пользователя')
    def test_create_new_user_success(self):
        """Проверяет успешное создание нового пользователя."""
        payload = User.create_data_user()
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=payload)
        logger.info(f"Создание пользователя: {response.status_code}, {response.text}")
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Создание пользователя, который уже есть в системе')
    def test_create_duplicate_user_error(self):
        """Проверяет, что при попытке создать уже существующего пользователя возвращается ошибка."""
        payload = User.data_double
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=payload)
        logger.warning(f"Создание дубля: {response.status_code}, {response.text}")
        assert response.status_code == 403
        assert "User already exists" in response.text

    @allure.title('Создание пользователя с некорректными данными')
    @pytest.mark.parametrize("user_data", [
        User.data_without_email,
        User.data_without_password,
        User.data_without_name
    ])
    def test_create_user_with_missing_fields(self, user_data):
        """Проверяет, что создание пользователя без обязательных полей вызывает ошибку."""
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=user_data)
        logger.warning(f"Некорректные данные: {response.status_code}, {response.text}")
        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.text

