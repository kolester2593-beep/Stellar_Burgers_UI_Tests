"""
Класс для страницы авторизации.
Этот класс инкапсулирует всю логику работы со страницей входа:
- Поиск и заполнение полей email и пароль
- Нажатие кнопки «Войти»
- Проверка успешной авторизации
Наследуется от BasePage и получает все его методы.
"""

from pages.base_page import BasePage

import allure


from locators.base_locators import (
    LOCATOR_PERSONAL_CABINET_BTN
)

from locators.main_locators import (
    LOCATOR_LOGIN_BUTTON,
    LOCATOR_BUTTON_PLACE_ORDER
)

from locators.login_locators import (
    LOCATOR_INPUT_EMAIL,
    LOCATOR_INPUT_PASSWORD,
    LOCATOR_BUTTON_LOGIN,
    LOCATOR_HEADER_LOGIN
)


class LoginPage(BasePage):


    # МЕТОДЫ ДЛЯ ПОЛЕЙ ВВОДА
    
    @allure.step("Ввод email: {email}")
    def input_email(self, email):
        self.input_text(LOCATOR_INPUT_EMAIL, email)

    @allure.step("Ввод пароля")
    def input_password(self, password):
        self.input_text(LOCATOR_INPUT_PASSWORD, password)
    

    # МЕТОДЫ ДЛЯ КНОПОК

    @allure.step("Нажатие кнопки «Войти»")
    def click_login_button(self):
        self.click(LOCATOR_BUTTON_LOGIN)
    
    @allure.step("Нажатие кнопки «Войти в аккаунт» на главной")
    def click_login_button_main(self):
        self.click(LOCATOR_PERSONAL_CABINET_BTN)


    # МЕТОДЫ ПРОВЕРКИ
    
    @allure.step("Проверка загрузки страницы входа")
    def is_login_page_loaded(self):
        return self.is_element_visible(LOCATOR_HEADER_LOGIN)
    
    @allure.step("Проверка видимости кнопки «Оформить заказ»")
    def is_place_order_button_visible(self):
        return self.is_element_visible(LOCATOR_BUTTON_PLACE_ORDER)
    
    @allure.step("Проверка видимости кнопки «Войти в аккаунт»")
    def is_login_button_main_visible(self):
        return self.is_element_visible(LOCATOR_LOGIN_BUTTON)
    

    # КОМПЛЕКСНЫЕ МЕТОДЫ

    
    @allure.step("Полная авторизация: email={email}")
    def login(self, email, password):
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()
        