import allure
import requests
import logging

from data.handlers import Urls, Handlers
from data.user_data import User

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@allure.suite('Авторизация пользователя')
class TestLogin:

    @allure.title('Авторизация под пользователем, который есть в системе')
    def test_login_returns_200_for_valid_user(self):
        """Проверяет, что авторизация с корректными данными проходит успешно."""
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.LOGIN}', data=User.data_correct)
        logger.info(f"Успешная авторизация: {response.status_code}, {response.text}")
        assert response.status_code == 200
        assert response.json().get('success') is True

    @allure.title('Авторизация с некорректным логином/паролем')
    def test_login_returns_401_for_invalid_user(self):
        """Проверяет, что авторизация с некорректными данными возвращает ошибку."""
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.LOGIN}', data=User.data_negative)
        logger.warning(f"Ошибка авторизации: {response.status_code}, {response.text}")
        assert response.status_code == 401
        assert response.json().get('success') is False
