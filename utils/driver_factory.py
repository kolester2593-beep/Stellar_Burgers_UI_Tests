import sys
import os

# Получаем абсолютный путь к корню проекта (на 2 уровня выше этого файла)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Добавляем корень в sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.config import Config

def get_driver(browser_name: str=Config.DEFAULT_BROWSERS):
    browser_name = browser_name.lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        # Отключаем уведомления
        options.add_argument("--disable-notifications")
        # Отключаем всплывающие подсказки и инфобары
        options.add_argument("--disabler-infobars")
        # Устанавливаем размер окна 
        options.add_argument("--window-size=1920,1080")
        # Устанавливаем язык интерфейса
        options.add_argument("--lang=ru-RU")

        # Создаём драйвер с автоматической загрузкой chromedriver
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser_name == "firefox":
        options = FirefoxOptions()
        # Устанавливаем размер окна
        options.add_argument("--width=1920")
        options.add_argument("--height=1920")
        # Отключаем автоматические обновления
        options.set_preference("app.update.auto", False)
        options.set_preference("app.update.enabled", False)
        # Устанавливаем язык 
        options.set_preference("intl.accept_languages", "ru-RU")
        # Создаём драйвер с автоматической загрузкой geckodriver
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )


    else:
        raise ValueError(
            f"Браузер '{browser_name}' не поддерживается."
            f"Доступные: {Config.BROWSERS}"
        )
    
    # Максимальное время загрузки страницы
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    # Неявное ожидание
    driver.implicitly_wait(Config.IMPLICIT_WAIT_TIMEOUT)
    # Разворачиваем окно на весь экран
    driver.maximize_window()

    return driver
