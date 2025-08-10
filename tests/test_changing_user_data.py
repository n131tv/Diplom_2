import allure
import requests
import uuid
import logging
from data.handlers import Urls, Handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


@allure.suite('Изменение данных пользователя')
class TestChangingUserData:

    @allure.title("Успешное изменение email авторизованного пользователя")
    def test_changing_user_email_with_auth(self, create_user):
        new_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        payload = {"email": new_email}
        headers = {"Authorization": create_user}

        response = requests.patch(
            f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",
            headers=headers,
            json=payload
        )

        logger.info(f"Статус ответа: {response.status_code}")
        logger.info(f"Тело ответа: {response.text}")

        assert response.status_code == 200, "Ожидался статус 200"
        assert response.json()["user"]["email"] == new_email, "Email не обновился корректно"




