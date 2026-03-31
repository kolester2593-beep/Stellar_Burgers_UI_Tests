"""
Класс для главной страницы (Конструктор бургеров).
Этот класс инкапсулирует всю логику работы с главной страницей:
- Навигация по хедеру (Конструктор, Лента заказов, Личный кабинет)
- Работа с табами ингредиентов (Булки, Соусы, Начинки)
- Работа с карточками ингредиентов
- Открытие/закрытие модальных окон ингредиентов
Наследуется от BasePage и получает все его методы.
Важно:
- Главная страница = страница конструктора (https://stellarburgers.education-services.ru/)
- ConstructorPage содержит методы для работы с корзиной/заказом
- MainPage содержит методы для работы с навигацией и списком ингредиентов
"""

from pages.base_page import BasePage

import allure

from locators.base_locators import (
    LOCATOR_CONSTRUCTOR_TAB,
    LOCATOR_ORDERS_FEED_TAB,
    LOCATOR_PERSONAL_CABINET_BTN,
    LOCATOR_MODAL_CONTAINER,
    LOCATOR_MODAL_TITLE,
    LOCATOR_MODAL_CLOSE_BUTTON
)

from locators.main_locators import (
    LOCATOR_CONSTRUCTOR_TITLE,
    LOCATOR_BUNS_TAB,
    LOCATOR_SAUCE_TAB,
    LOCATOR_FILLING_TAB,
    LOCATOR_ACTIVE_TAB,
    LOCATOR_INGREDIENT_CARD,
    LOCATOR_INGREDIENT_NAME,
    LOCATOR_LOGIN_BUTTON,
    LOCATOR_BUTTON_PLACE_ORDER
)

from locators.constructor_locators import (
    LOCATOR_INGREDIENT_CARD
)


class MainPage(BasePage):


    # МЕТОДЫ НАВИГАЦИИ
    
    @allure.step("Открытие главной страницы")
    def open_main_page(self):
        self.open(self.BASE_URL)
    
    @allure.step("Переход на страницу ленты заказов")
    def go_to_orders_feed(self):
        self.click(LOCATOR_ORDERS_FEED_TAB)
    
    @allure.step("Переход на страницу конструктора")
    def go_to_constructor(self):
        self.click(LOCATOR_CONSTRUCTOR_TAB)    
    
    @allure.step("Открытие модального окна авторизации")
    def open_login_modal(self):
        self.click(LOCATOR_PERSONAL_CABINET_BTN) 
    
    @allure.step("Проверка текущего таба: {tab_name}")
    def is_current_tab(self, tab_name):
        if tab_name == "Конструктор":
            return self.is_element_visible(LOCATOR_CONSTRUCTOR_TAB)
        elif tab_name == "Лента Заказов":
            return self.is_element_visible(LOCATOR_ORDERS_FEED_TAB)
        
        return False


    # МЕТОДЫ РАБОТЫ С ТАБАМИ ИНГРЕДИЕНТОВ
    
    @allure.step("Переключение на таб «Булки»")
    def switch_to_buns_tab(self):
        self.click(LOCATOR_BUNS_TAB)    
    
    @allure.step("Переключение на таб «Соусы»")
    def switch_to_sauce_tab(self):
        self.click(LOCATOR_SAUCE_TAB)
    
    @allure.step("Переключение на таб «Начинки»")
    def switch_to_filling_tab(self):
        self.click(LOCATOR_FILLING_TAB)
    
    @allure.step("Проверка активного таба ингредиентов")
    def get_active_tab(self):
        active_tab = self.find_element(LOCATOR_ACTIVE_TAB)
        return active_tab.text
    

    # МЕТОДЫ РАБОТЫ С ИНГРЕДИЕНТАМИ
    
    @allure.step("Получение списка всех ингредиентов")
    def get_all_ingredients(self):
        return self.find_elements(LOCATOR_INGREDIENT_CARD)
    
    @allure.step("Получение количества ингредиентов")
    def get_ingredients_count(self):
        return len(self.get_all_ingredients())
    
    @allure.step("Получение ингредиента по индексу: {index}")
    def get_ingredient_by_index(self, index):
        ingredients = self.get_all_ingredients()
        return ingredients[index]
    
    @allure.step("Получение ингредиента по названию: {name}")
    def get_ingredient_by_name(self, name):
        ingredients = self.get_all_ingredients()
        
        for ingredient in ingredients:
            name_element = ingredient.find_element(LOCATOR_INGREDIENT_NAME)
            if name_element.text == name:
                return ingredient
        
        return None
    
    @allure.step("Получение названия ингредиента по индексу: {index}")
    def get_ingredient_name(self, index=0):
        ingredient = self.get_ingredient_by_index(index)
        name_element = ingredient.find_element(LOCATOR_INGREDIENT_NAME)
        return name_element.text
    
    # МЕТОДЫ РАБОТЫ С МОДАЛЬНЫМИ ОКНАМИ

    
    @allure.step("Открытие модального окна ингредиента: индекс {index}")
    def open_ingredient_modal(self, index=0):
        ingredient = self.get_ingredient_by_index(index)
        self._execute_script("arguments[0].click();", ingredient)
        # Ждём появления модального окна
        self.wait_for_element_visible(LOCATOR_MODAL_CONTAINER)
    
    @allure.step("Открытие модального окна ингредиента по названию: {name}")
    def open_ingredient_modal_by_name(self, name):
        ingredient = self.get_ingredient_by_name(name)
        if ingredient is None:
            raise ValueError(f"Ингредиент '{name}' не найден")
        ingredient.click()
        self.wait_for_element_visible(LOCATOR_MODAL_CONTAINER)
    
    @allure.step("Проверка открытого модального окна")
    def is_modal_open(self):
        return self.is_element_visible(LOCATOR_MODAL_CONTAINER)
    
    @allure.step("Получение названия ингредиента из модального окна")
    def get_modal_ingredient_name(self):
        return self.get_text(LOCATOR_MODAL_TITLE)
    
    @allure.step("Закрытие модального окна ингредиента")
    def close_ingredient_modal(self):
        self.click(LOCATOR_MODAL_CLOSE_BUTTON) 
        # Ждём исчезновения модального окна
        self.wait_for_element_disappear(LOCATOR_MODAL_CONTAINER)
    

    # МЕТОДЫ ПРОВЕРКИ СОСТОЯНИЯ СТРАНИЦЫ
    
    @allure.step("Проверка загрузки главной страницы")
    def is_main_page_loaded(self, timeout=10):
        try:
            self.wait_for_element_visible(LOCATOR_CONSTRUCTOR_TITLE, timeout=timeout)
            return True
        except:
            return False
        
    @allure.step("Проверка видимости кнопки «Войти в аккаунт»")
    def is_login_button_visible(self):
        return self.is_element_visible(LOCATOR_LOGIN_BUTTON)
    
    @allure.step("Проверка видимости кнопки «Оформить заказ»")
    def is_order_button_visible(self):
        return self.is_element_visible(LOCATOR_BUTTON_PLACE_ORDER)