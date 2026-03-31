"""
Класс для страницы авторизации.
Этот класс инкапсулирует всю логику работы со страницей входа:
- Поиск и заполнение полей email и пароль
- Нажатие кнопки «Войти»
- Проверка успешной авторизации
Наследуется от BasePage и получает все его методы.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

import allure


class LoginPage(BasePage):

    
    # --- Кнопки навигации (на главной странице) ---
    
    # Кнопка «Войти в аккаунт» на главной странице
    BUTTON_LOGIN_MAIN = (By.XPATH, "//button[text()='Войти в аккаунт']")
    # Кнопка «Оформить заказ» на главной странице (после авторизации)
    BUTTON_PLACE_ORDER = (By.XPATH, "//button[text()='Оформить заказ']")
    
    # --- Элементы страницы входа (/login) ---
    
    # Плейсхолдер поля Email
    LABEL_EMAIL = (By.XPATH, "//label[text()='Email']")
    
    # Плейсхолдер поля Пароль
    LABEL_PASSWORD = (By.XPATH, "//label[text()='Пароль']")
    
    # Поле ввода Email (name='name')
    INPUT_EMAIL = (By.XPATH, "//input[@name='name']")
    
    # Поле ввода Пароля (name='Пароль')
    INPUT_PASSWORD = (By.XPATH, "//input[@name='Пароль']")
    
    # Кнопка «Войти»
    BUTTON_LOGIN = (By.XPATH, "//button[text()='Войти']")
    
    # Заголовок страницы «Вход»
    HEADER_LOGIN = (By.XPATH, "//h2[text()='Вход']")
    

    # МЕТОДЫ ДЛЯ ПОЛЕЙ ВВОДА
    
    @allure.step("Ввод email: {email}")
    def input_email(self, email):
        self.input_text(self.INPUT_EMAIL, email)

    @allure.step("Ввод пароля")
    def input_password(self, password):
        self.input_text(self.INPUT_PASSWORD, password)
    

    # МЕТОДЫ ДЛЯ КНОПОК

    @allure.step("Нажатие кнопки «Войти»")
    def click_login_button(self):
        self.click(self.BUTTON_LOGIN)
    
    @allure.step("Нажатие кнопки «Войти в аккаунт» на главной")
    def click_login_button_main(self):
        self.click(self.BUTTON_LOGIN_MAIN)


    # МЕТОДЫ ПРОВЕРКИ
    
    @allure.step("Проверка загрузки страницы входа")
    def is_login_page_loaded(self):
        return self.is_element_visible(self.HEADER_LOGIN)
    
    @allure.step("Проверка видимости кнопки «Оформить заказ»")
    def is_place_order_button_visible(self):
        return self.is_element_visible(self.BUTTON_PLACE_ORDER)
    
    @allure.step("Проверка видимости кнопки «Войти в аккаунт»")
    def is_login_button_main_visible(self):
        return self.is_element_visible(self.BUTTON_LOGIN_MAIN)
    

    # КОМПЛЕКСНЫЕ МЕТОДЫ

    
    @allure.step("Полная авторизация: email={email}")
    def login(self, email, password):
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()
        