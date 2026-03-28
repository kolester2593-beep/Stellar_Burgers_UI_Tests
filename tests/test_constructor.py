"""
Тестируемая функциональность:
1. Переход по клику на «Конструктор»
2. Переход по клику на раздел «Лента заказов»
3. Открытие модального окна ингредиента при клике
4. Закрытие модального окна кликом по крестику
5. Увеличение счётчика ингредиента при добавлении в заказ
Все тесты НЕ требуют авторизации.
"""

import allure
import pytest


@allure.feature("Конструктор бургеров")
@allure.story("Навигация")
class TestNavigation:

    
    @allure.title("Переход по клику на «Конструктор»")
    def test_go_to_constructor_page(self, main_page):

        # Открываем главную страницу
        main_page.open_main_page()
        
        # Кликаем по табу «Конструктор»
        main_page.go_to_constructor()
        
        # Проверяем, что страница конструктора загружена
        assert main_page.is_main_page_loaded(), "Страница конструктора не загрузилась"
    
    @allure.title("Переход по клику на раздел «Лента заказов»")
    def test_go_to_orders_feed_page(self, main_page):
        # Открываем главную страницу
        main_page.open_main_page()
        
        # Кликаем по табу «Лента заказов»
        main_page.go_to_orders_feed()
        
        # Проверяем заголовок страницы (через URL или элемент)
        # Проверяем, что URL содержит /feed
        assert "/feed" in main_page.get_current_url(), "Переход на страницу ленты заказов не выполнен"


@allure.feature("Конструктор бургеров")
@allure.story("Модальные окна")
class TestIngredientModal:

    
    @allure.title("Открытие всплывающего окна с деталями ингредиента")
    def test_open_ingredient_modal(self, main_page):

        # Открываем главную страницу
        main_page.open_main_page()
        
        # Открываем модальное окно первого ингредиента
        main_page.open_ingredient_modal(index=0)
        
        # Проверяем, что модальное окно открыто
        assert main_page.is_modal_open(), "Модальное окно ингредиента не открылось"
    
    @allure.title("Закрытие всплывающего окна кликом по крестику")
    def test_close_ingredient_modal_by_cross(self, main_page):

        # Открываем главную страницу и модальное окно
        main_page.open_main_page()
        main_page.open_ingredient_modal(index=0)
        
        # Закрываем модальное окно кликом по крестику
        main_page.close_ingredient_modal()
        
        # Проверяем, что модальное окно закрыто
        assert not main_page.is_modal_open(), "Модальное окно не закрылось после клика по крестику"


@allure.feature("Конструктор бургеров")
@allure.story("Счётчики ингредиентов")
class TestIngredientCounter:

    
    @allure.title("Увеличение счётчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increases_on_add(self, constructor_page, request):

        # Открываем страницу конструктора
        constructor_page.open_constructor_page()
        
        # Получаем начальное значение счётчика
        initial_counter = constructor_page.get_counter_value(index=0)
        
        # Определяем браузер из параметризации
        browser = request.node.get_closest_marker("browser")
        
        # Добавляем ингредиент (разный метод для разных браузеров)
        if "firefox" in request.node.name.lower():
            # Для Firefox используем JavaScript
            constructor_page.drag_ingredient_to_constructor_js(index=0)
        else:
            # Для Chrome используем ActionChains
            constructor_page.drag_ingredient_to_constructor(index=0)
        
        # Ждём увеличения счётчика (увеличили таймаут для Firefox)
        constructor_page.wait_for_counter_increase(
            index=0, 
            old_value=str(initial_counter),
            timeout=15  # Увеличенный таймаут
        )
        
        # Получаем новое значение счётчика
        new_counter = constructor_page.get_counter_value(index=0)
        
        # Проверяем, что счётчик увеличился
        assert new_counter == initial_counter + 2, (
            f"Счётчик не увеличился. Было: {initial_counter}, стало: {new_counter}"
        )