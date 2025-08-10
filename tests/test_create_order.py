import allure
import requests
import logging
import pytest

from data.handlers import Urls, Handlers
from data.ingredients_data import Ingredient

# Настройка логгера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_auth(self, create_user):
        """Проверяет, что авторизованный пользователь может создать заказ."""
        with allure.step("Получаем токен авторизованного пользователя"):
            token = {'Authorization': create_user[3]}  # Предполагается, что create_user возвращает кортеж с токеном

        with allure.step("Отправляем запрос на создание заказа"):
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
                headers=token,
                json=Ingredient.correct_ingredients_data  # Используем json вместо data для JSON-данных
            )

        logger.info(f"Ответ авторизованного запроса: {response.status_code}, {response.text}")

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
            assert response.json().get("success") is True, "Флаг success не равен True"

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_not_auth(self):
        """Проверяет, что неавторизованный пользователь может создать заказ."""
        with allure.step("Отправляем запрос без токена авторизации"):
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
                json=Ingredient.correct_ingredients_data
            )

        logger.info(f"Ответ неавторизованного запроса: {response.status_code}, {response.text}")

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
            assert response.json().get("success") is True, "Флаг success не равен True"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        """Проверяет, что заказ без ингредиентов не может быть создан."""
        with allure.step("Отправляем запрос без данных об ингредиентах"):
            response = requests.post(f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}")

        logger.info(f"Ответ запроса без ингредиентов: {response.status_code}, {response.text}")

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
            assert response.json().get("message") == "Ingredient ids must be provided", "Неверное сообщение об ошибке"

    @allure.title("Создание заказа с невалидным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self):
        """Проверяет, что заказ с невалидным хешем ингредиента вызывает ошибку сервера."""
        with allure.step("Отправляем запрос с невалидными ингредиентами"):
            response = requests.post(
                f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
                headers=Handlers.headers,
                json=Ingredient.incorrect_ingredients_data
            )

        logger.warning(f"Ответ запроса с невалидным ингредиентом: {response.status_code}, {response.text}")

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 500, f"Ожидался статус 500, получен {response.status_code}"
            assert "Internal Server Error" in response.text, "Отсутствует сообщение об ошибке сервера"

