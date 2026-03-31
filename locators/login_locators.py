""" Локаторы для LoginPage """

from selenium.webdriver.common.by import By


# --- Элементы страницы входа (/login) ---

# Поле ввода Email (name='name')
LOCATOR_INPUT_EMAIL = (By.XPATH, "//input[@name='name']")

# Поле ввода Пароля (name='Пароль')
LOCATOR_INPUT_PASSWORD = (By.XPATH, "//input[@name='Пароль']")

# Кнопка «Войти»
LOCATOR_BUTTON_LOGIN = (By.XPATH, "//button[text()='Войти']")

# Заголовок страницы «Вход»
LOCATOR_HEADER_LOGIN = (By.XPATH, "//h2[text()='Вход']")