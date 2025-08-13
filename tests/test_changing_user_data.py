import allure
import requests
import uuid
import logging
from data.handlers import Urls, Handlers

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


@allure.suite("Изменение данных пользователя")
@allure.feature("Обновление email")
class TestChangingUserData:

    @allure.title("Успешное изменение email авторизованного пользователя")
    @allure.description("Проверка, что авторизованный пользователь может изменить свой email и получить обновлённые данные")
    def test_changing_user_email_with_auth(self, create_user):
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
