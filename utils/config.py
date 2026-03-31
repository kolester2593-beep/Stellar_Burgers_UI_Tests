# Глобальные настройки проекта, разделённые по ответственности


# Настройки приложения (URL, базовые параметры)
class AppConfig:

    # URL приложения
    BASE_URL = "https://stellarburgers.education-services.ru/"


# КЛАСС 2: Настройки таймаутов и ожиданий
class TimeoutConfig:

    # Время ожидания загрузки страницы
    PAGE_LOAD_TIMEOUT = 15
    # Стандартное время для явных ожиданий (WebDriverWait)
    EXPLICIT_WAIT_TIMEOUT = 10
    # Время для неявных ожиданий (driver.implicitly_wait)
    IMPLICIT_WAIT_TIMEOUT = 10


# Настройки браузеров
class BrowserConfig:

    BROWSERS = ['chrome', 'firefox']
    DEFAULT_BROWSERS = 'chrome'


# Тестовые данные
class TestData:

    USER_EMAIL = "testovii@test.ru"
    USER_PASSWORD = "pass123word"
    USER_NAME = "Тестировщик"
