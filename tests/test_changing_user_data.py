import allure
import requests
import uuid

from data.handlers import Urls, Handlers
from data.user_data import User


@allure.suite('Изменение данных пользователя')
class TestChangingUserData:

    @allure.description("При попытке сменить email у авторизованного пользователя, изменение данных происходит успешно")
    @allure.title("Успешное изменение email авторизованного пользователя")
    def test_changing_user_email_with_auth(self, create_user):
        unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        payload = {'email': unique_email}
        token = {'Authorization': create_user[3]}

        r = requests.patch(
            f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
            headers=token,
            json=payload  # Важно использовать json
        )

        print("EMAIL CHANGE STATUS:", r.status_code)
        print("EMAIL CHANGE RESPONSE:", r.text)

        assert r.status_code == 200
        assert r.json()['user']['email'] == payload["email"]

    @allure.description("При попытке сменить password у авторизованного пользователя, изменение данных происходит успешно")
    @allure.title("Успешное изменение password авторизованного пользователя")
    def test_changing_user_password_with_auth(self, create_user):
        payload = {'password': User.create_data_user()["password"]}
        token = {'Authorization': create_user[3]}

        r = requests.patch(
            f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
            headers=token,
            json=payload
        )

        print("PASSWORD CHANGE STATUS:", r.status_code)
        print("PASSWORD CHANGE RESPONSE:", r.text)

        assert r.status_code == 200
        assert r.json().get("success") is True

    @allure.description("При попытке сменить name у авторизованного пользователя, изменение данных происходит успешно")
    @allure.title("Успешное изменение name авторизованного пользователя")
    def test_changing_user_name_with_auth(self, create_user):
        payload = {'name': User.create_data_user()["name"]}
        token = {'Authorization': create_user[3]}

        r = requests.patch(
            f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
            headers=token,
            json=payload
        )

        print("NAME CHANGE STATUS:", r.status_code)
        print("NAME CHANGE RESPONSE:", r.text)

        assert r.status_code == 200
        assert r.json()['user']['name'] == payload["name"]

    @allure.description("При попытке смены данных пользователя без авторизации, возвращается ошибка")
    @allure.title("Изменение данных пользователя без авторизации")
    def test_changing_user_data_not_auth(self):
        r = requests.patch(
            f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
            json=User.create_data_user()
        )

        print("UNAUTHORIZED CHANGE STATUS:", r.status_code)
        print("UNAUTHORIZED CHANGE RESPONSE:", r.text)

        assert r.status_code == 401
        assert r.json()['message'] == 'You should be authorised'
