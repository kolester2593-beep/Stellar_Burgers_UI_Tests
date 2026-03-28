# Глобальные настройки проекта.
# Храним URL, таймауты и настройки браузеров в одном месте.
# Тестовые данные дял авторизации
class Config:


    # URL приложения
    BASE_URL = "https://stellarburgers.education-services.ru/"


    # ---Таймауты в секундах---

    # Время ожидания загрузки страницы
    PAGE_LOAD_TIMEOUT = 15
    # Стандартное время для явных ожиданий (WebDriverWait)
    EXPLICIT_WAIT_TIMEOUT = 10
    # Время для неявных ожиданий (driver.implicitly_wait)
    IMPLICIT_WAIT_TIMEOUT = 10


    # ---Настройки браузеров

    BROWSERS = ['chrome', 'firefox']
    DEFAULT_BROWSERS = 'chrome'


    # --- Тестовые данные дял авторизации ---

    USER_EMAIL = "testovii@test.ru"
    USER_PASSWORD = "pass123word"
    USER_NAME = "Тестировщик"

    