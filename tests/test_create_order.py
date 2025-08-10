import allure
import requests
import logging

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
        token = {'Authorization': create_user[3]}
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            headers=token,
            data=Ingredient.correct_ingredients_data
        )
        logger.info(f"Ответ авторизованного запроса: {response.status_code}, {response.text}")
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_not_auth(self):
        """Проверяет, что неавторизованный пользователь может создать заказ."""
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            data=Ingredient.correct_ingredients_data
        )
        logger.info(f"Ответ неавторизованного запроса: {response.status_code}, {response.text}")
        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        """Проверяет, что заказ без ингредиентов не может быть создан."""
        response = requests.post(f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}")
        logger.info(f"Ответ запроса без ингредиентов: {response.status_code}, {response.text}")
        assert response.status_code == 400
        assert response.json().get("message") == "Ingredient ids must be provided"

    @allure.title("Создание заказа с невалидным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self):
        """Проверяет, что заказ с невалидным хешем ингредиента вызывает ошибку сервера."""
        response = requests.post(
            f"{Urls.MAIN_URL}{Handlers.MAKE_ORDER}",
            headers=Handlers.headers,
            json=Ingredient.incorrect_ingredients_data
        )
        logger.warning(f"Ответ запроса с невалидным ингредиентом: {response.status_code}, {response.text}")
        assert response.status_code == 500
        assert "Internal Server Error" in response.text

