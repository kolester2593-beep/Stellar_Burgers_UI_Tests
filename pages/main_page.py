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

from selenium.webdriver.common.by import By

import allure

from pages.base_page import BasePage


class MainPage(BasePage):

    
    # --- Навигация (Header) ---
    
    # Кнопка «Конструктор» в хедере (активная страница)
    LOCATOR_CONSTRUCTOR_TAB = (By.LINK_TEXT, "Конструктор")
    
    # Кнопка «Лента Заказов» в хедере (переход на ленту заказов)
    LOCATOR_ORDERS_FEED_TAB = (By.LINK_TEXT, "Лента Заказов")
    
    # Кнопка «Личный Кабинет» в хедере (открывает модальное окно логина)
    LOCATOR_PERSONAL_CABINET_BTN = (By.CSS_SELECTOR, "a[href='/account']")
    
    # Логотип (ссылка на главную)
    LOCATOR_LOGO = (By.CSS_SELECTOR, ".AppHeader_header__logo__2D0X2 a")
    
    # --- Заголовок страницы ---
    
    # Заголовок «Соберите бургер»
    LOCATOR_PAGE_HEADER = (By.XPATH, "//h1[text()='Соберите бургер']")
    
    # --- Табы ингредиентов ---
    
    # Таб «Булки» (переключение на булки)
    LOCATOR_BUNS_TAB = (By.XPATH, "//span[text()='Булки']")
    
    # Таб «Соусы» (переключение на соусы)
    LOCATOR_SAUCE_TAB = (By.XPATH, "//span[text()='Соусы']")
    
    # Таб «Начинки» (переключение на начинки)
    LOCATOR_FILLING_TAB = (By.XPATH, "//span[text()='Начинки']")
    
    # Активный таб (имеет класс tab_tab_type_current__2BEPc)
    LOCATOR_ACTIVE_TAB = (By.CSS_SELECTOR, ".tab_tab_type_current__2BEPc")
    
    # --- Ингредиенты (карточки) ---
    
    # Карточка ингредиента (общий селектор для всех ингредиентов)
    LOCATOR_INGREDIENT_CARD = (By.CSS_SELECTOR, ".BurgerIngredient_ingredient__1TVf6")
    
    # Название ингредиента (текст под картинкой)
    LOCATOR_INGREDIENT_NAME = (By.CSS_SELECTOR, ".BurgerIngredient_ingredient__text__yp3dH")
    
    # Список ингредиентов (контейнер)
    LOCATOR_INGREDIENTS_LIST = (By.CSS_SELECTOR, ".BurgerIngredients_ingredients__list__2A-mT")

    
    # --- Модальное окно ингредиента ---
    
    # Контейнер модального окна
    LOCATOR_MODAL_CONTAINER = (By.CSS_SELECTOR, ".Modal_modal__container__Wo2l_")
    
    # Заголовок модального окна
    LOCATOR_MODAL_TITLE = (By.CSS_SELECTOR, ".Modal_modal__title__2L34m")
    
    # Кнопка закрытия модального окна (крестик)
    LOCATOR_MODAL_CLOSE_BTN = (By.CSS_SELECTOR, ".Modal_modal__close__TnseK")
    
    # Кнопка «Войти в аккаунт» (в конструкторе, когда не авторизован)
    LOCATOR_LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    
    # Кнопка «Оформить заказ» (в конструкторе, когда авторизован)
    LOCATOR_ORDER_BUTTON = (By.CSS_SELECTOR, ".BurgerConstructor_basket__container__2fUl3 .button_button_type_primary__1O7Bx")

    
    # МЕТОДЫ НАВИГАЦИИ
    
    @allure.step("Открытие главной страницы")
    def open_main_page(self):
        self.open(self.BASE_URL)
        return self
    
    @allure.step("Переход на страницу ленты заказов")
    def go_to_orders_feed(self):
        self.click(self.LOCATOR_ORDERS_FEED_TAB)
        return self
    
    @allure.step("Переход на страницу конструктора")
    def go_to_constructor(self):
        self.click(self.LOCATOR_CONSTRUCTOR_TAB)    
        return self
    
    @allure.step("Открытие модального окна авторизации")
    def open_login_modal(self):
        self.click(self.LOCATOR_PERSONAL_CABINET_BTN) 
        return self
    
    @allure.step("Проверка текущего таба: {tab_name}")
    def is_current_tab(self, tab_name):
        if tab_name == "Конструктор":
            return self.is_element_visible(self.LOCATOR_CONSTRUCTOR_TAB)
        elif tab_name == "Лента Заказов":
            return self.is_element_visible(self.LOCATOR_ORDERS_FEED_TAB)
        
        return False


    # МЕТОДЫ РАБОТЫ С ТАБАМИ ИНГРЕДИЕНТОВ
    
    @allure.step("Переключение на таб «Булки»")
    def switch_to_buns_tab(self):
        self.click(self.LOCATOR_BUNS_TAB)    
        return self
    
    @allure.step("Переключение на таб «Соусы»")
    def switch_to_sauce_tab(self):
        self.click(self.LOCATOR_SAUCE_TAB)
        return self
    
    @allure.step("Переключение на таб «Начинки»")
    def switch_to_filling_tab(self):
        self.click(self.LOCATOR_FILLING_TAB)
        return self
    
    @allure.step("Проверка активного таба ингредиентов")
    def get_active_tab(self):
        active_tab = self.find_element(self.LOCATOR_ACTIVE_TAB)
        return active_tab.text
    

    # МЕТОДЫ РАБОТЫ С ИНГРЕДИЕНТАМИ
    
    @allure.step("Получение списка всех ингредиентов")
    def get_all_ingredients(self):
        return self.find_elements(self.LOCATOR_INGREDIENT_CARD)
    
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
            name_element = ingredient.find_element(*self.LOCATOR_INGREDIENT_NAME)
            if name_element.text == name:
                return ingredient
        
        return None
    
    @allure.step("Получение названия ингредиента по индексу: {index}")
    def get_ingredient_name(self, index=0):
        ingredient = self.get_ingredient_by_index(index)
        name_element = ingredient.find_element(*self.LOCATOR_INGREDIENT_NAME)
        return name_element.text
    
    # МЕТОДЫ РАБОТЫ С МОДАЛЬНЫМИ ОКНАМИ

    
    @allure.step("Открытие модального окна ингредиента: индекс {index}")
    def open_ingredient_modal(self, index=0):
        ingredient = self.get_ingredient_by_index(index)
        self.driver.execute_script("arguments[0].click();", ingredient)
        # Ждём появления модального окна
        self.wait_for_element_visible(self.LOCATOR_MODAL_CONTAINER)
        return self
    
    @allure.step("Открытие модального окна ингредиента по названию: {name}")
    def open_ingredient_modal_by_name(self, name):
        ingredient = self.get_ingredient_by_name(name)
        if ingredient is None:
            raise ValueError(f"Ингредиент '{name}' не найден")
        ingredient.click()
        self.wait_for_element_visible(self.LOCATOR_MODAL_CONTAINER)
        return self
    
    @allure.step("Проверка открытого модального окна")
    def is_modal_open(self):
        return self.is_element_visible(self.LOCATOR_MODAL_CONTAINER)
    
    @allure.step("Получение названия ингредиента из модального окна")
    def get_modal_ingredient_name(self):
        return self.get_text(self.LOCATOR_MODAL_TITLE)
    
    @allure.step("Закрытие модального окна ингредиента")
    def close_ingredient_modal(self):
        self.click(self.LOCATOR_MODAL_CLOSE_BTN) 
        # Ждём исчезновения модального окна
        self.wait_for_element_disappear(self.LOCATOR_MODAL_CONTAINER)
        return self
    

    # МЕТОДЫ ПРОВЕРКИ СОСТОЯНИЯ СТРАНИЦЫ
    
    @allure.step("Проверка загрузки главной страницы")
    def is_main_page_loaded(self):
        return self.is_element_visible(self.LOCATOR_PAGE_HEADER)
    
    @allure.step("Проверка видимости кнопки «Войти в аккаунт»")
    def is_login_button_visible(self):
        return self.is_element_visible(self.LOCATOR_LOGIN_BUTTON)
    
    @allure.step("Проверка видимости кнопки «Оформить заказ»")
    def is_order_button_visible(self):
        return self.is_element_visible(self.LOCATOR_ORDER_BUTTON)