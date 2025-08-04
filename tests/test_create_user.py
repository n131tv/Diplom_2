import pytest
import allure
import requests

from data.handlers import Urls, Handlers
from data.user_data import User


@allure.suite('Создание пользователя')
class TestCreateUser:

    @allure.description('Создание нового пользователя')
    @allure.title('Создание нового пользователя')
    def test_create_new_user_success(self):
        payload = User.create_data_user()
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=payload)
        print("Создание пользователя:", response.status_code, response.text)
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.description('При создании дублирующего пользователя возвращается сообщение об ошибке')
    @allure.title('Создание пользователя, который уже есть в системе')
    def test_create_double_user_error(self):
        payload = User.data_double
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=payload)
        print("Создание дубля:", response.status_code, response.text)
        assert response.status_code == 403
        assert "User already exists" in response.text

    @allure.description('Проверка ошибок при создании пользователя с отсутствием обязательных полей')
    @allure.title('Создание пользователя с некорректными данными')
    @pytest.mark.parametrize("user_data", [
        User.data_without_email,
        User.data_without_password,
        User.data_without_name
    ])
    def test_create_user_incorrect_data(self, user_data):
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=user_data)
        print("Некорректные данные:", response.status_code, response.text)
        assert response.status_code == 403
        assert "Email, password and name are required fields" in response.text
