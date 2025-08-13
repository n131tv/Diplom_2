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
    def test_login_user_success(self):
        """Проверяет успешную авторизацию с корректными данными."""
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.LOGIN}', data=User.data_correct)
        logger.info(f"Успешная авторизация: {response.status_code}, {response.text}")
        assert response.status_code == 200
        assert response.json().get('success') is True

    @allure.title('Авторизация с некорректным логином/паролем')
    def test_login_user_invalid_credentials(self):
        """Проверяет, что при авторизации с некорректными данными возвращается ошибка."""
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.LOGIN}', data=User.data_negative)
        logger.warning(f"Ошибка авторизации: {response.status_code}, {response.text}")
        assert response.status_code == 401
        assert response.json().get('success') is False
