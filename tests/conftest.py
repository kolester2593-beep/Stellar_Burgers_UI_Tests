import pytest
import allure

from utils.config import Config
from utils.driver_factory import get_driver

from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.orders_feed_page import OrdersFeedPage
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# ФИКСТУРА ДРАЙВЕРА (ОСНОВНАЯ)
@pytest.fixture(params=Config.BROWSERS, scope='function')
@allure.feature('Инфраструктура')
@allure.story('Инициализация браузера')
def driver(request):
    browser_name = request.param

    with allure.step(f'Инициализация браузера: {browser_name.upper()}'):
        driver_instance = get_driver(browser_name)

    test_name = request.node.name
    allure.dynamic.title(f"Тест: {test_name} [{browser_name.upper()}]")
    allure.dynamic.tag (f"Браузер: {browser_name}")

    with allure.step("Отчистка состояния перед тестом"):
        # Открываем базовый URL
        driver_instance.get(Config.BASE_URL)
        # Отчищаем куки
        driver_instance.delete_all_cookies()
        # Отчищаем локальное хранилище
        driver_instance.execute_script("localStorage.clear();")
        # Отчищаем сеансы
        driver_instance.execute_script("sessionStorage.clear();")

    yield driver_instance

    with allure.step("Завершение работы браузера"):
        driver_instance.quit()


# ФИКСТУРЫ ДЛЯ PAGE OBJECT

# Фикстура для главной страницы
@pytest.fixture(scope="function")
@allure.feature("PageObjects")
@allure.story("Главная страница")
def main_page(driver):

    with allure.step("Инициализация MainPage"):
        page = MainPage(driver)

    return page

# Фикстура для страницы ленты заказов
@pytest.fixture(scope="function")
@allure.feature("PageObjects")
@allure.story("Страница ленты заказов")
def constructor_page(driver):

    with allure.step("Инициализация ConstructorPage"):
        page = ConstructorPage(driver)
    
    return page

# Фикстура для ленты заказов
@pytest.fixture(scope="function")
@allure.feature("Page Objects")
@allure.story("Страница ленты заказов")
def orders_feed_page(driver):

    with allure.step("Инициализация OrdersFeedPage"):
        page = OrdersFeedPage(driver)

    return page


@pytest.fixture(scope="function")
@allure.feature("Page Objects")
@allure.story("Страница авторизации")
def login_page(driver):
    
    with allure.step("Инициализация LoginPage"):
        page = LoginPage(driver)
    
    return page


# ДОПОЛНИТЕЛЬНЫЕ ВСПОМОГАТЕЛЬНЫЕ ФИКСТУРЫ 

@pytest.fixture(scope="function")
@allure.feature("Утилита")
@allure.story("Навигация")
def navigate_to_main(driver):

    with allure.step("Переход на главную страницу"):
        driver.get(Config.BASE_URL)

    yield driver

@pytest.fixture(scope="function")
@allure.feature("Утилиты")
@allure.story('Ожидание')
def wait(driver):

    with allure.step ("Инициализация WebDriverWait"):
        wait_instance = WebDriverWait(driver, Config.EXPLICIT_WAIT_TIMEOUT)

    return wait_instance


# ФИКСТУРЫ АВТОРИЗАЦИЙ

@pytest.fixture(scope="function")
@allure.feature("Авторизация")
@allure.story("Вход для тестов ленты заказов")
def login_user(main_page, login_page):
    
    with allure.step("Авторизация пользователя перед тестом"):
        
        # Шаг 1: Открываем главную страницу
        with allure.step("Открытие главной страницы"):
            main_page.open_main_page()
        
        # Шаг 2: Открываем форму входа (клик по «Личный Кабинет»)
        with allure.step("Открытие модального окна авторизации"):
            main_page.open_login_modal()
        
        # Шаг 3: Вводим данные для входа
        with allure.step(f"Ввод email: {Config.USER_EMAIL}"):
            login_page.input_email(Config.USER_EMAIL)
        
        with allure.step("Ввод пароля"):
            login_page.input_password(Config.USER_PASSWORD)
        
        # Шаг 4: Нажимаем кнопку «Войти»
        with allure.step("Нажатие кнопки «Войти»"):
            login_page.click_login_button()
        
        # Шаг 5: Проверяем успешную авторизацию
        with allure.step("Проверка успешной авторизации"):
            # Ждём появления кнопки «Оформить заказ» (признак авторизации)
            main_page.wait_for_element_clickable(
                main_page.LOCATOR_ORDER_BUTTON, 
                timeout=10
            )
    
    yield


@pytest.fixture(scope="function")
@allure.feature("Создание заказа")
@allure.story("Подготовка данных для тестов ленты заказов")
def create_order(login_user, constructor_page):
    
    with allure.step("Создание тестового заказа"):
        
        # === Шаг 1: Краторная булка (счётчик станет 2) ===
        with allure.step("Добавление Краторной булки"):
            constructor_page.drag_ingredient_to_constructor_by_locator(
                constructor_page.LOCATOR_KRATOR_BUN
            )
            # Булка добавляется дважды (верх+низ)
            assert constructor_page.get_krator_bun_counter() == 2, "Счётчик булки не равен 2"
        
        # === Шаг 2: Соус Spicy-X (1 раз) ===
        with allure.step("Добавление Соуса Spicy-X"):
            constructor_page.drag_ingredient_to_constructor_by_locator(
                constructor_page.LOCATOR_SPICY_SAUCE
            )
            assert constructor_page.get_spicy_sauce_counter() == 1, "Счётчик соуса не равен 1"
        
        # === Шаг 3: Переключаемся на вкладку "Начинки" ===
        with allure.step("Переключение на вкладку «Начинки»"):
            constructor_page.click(constructor_page.LOCATOR_FILLINGS_TAB)
        
        # === Шаг 4-6: Добавляем начинки ===
        for name, locator, counter_method in [
            ("Говяжий метеорит", constructor_page.LOCATOR_BEEF_METEORITE, constructor_page.get_beef_meteorite_counter),
            ("Хрустящие кольца", constructor_page.LOCATOR_CRISPY_RINGS, constructor_page.get_crispy_rings_counter),
            ("Плоды Фалленианского дерева", constructor_page.LOCATOR_FALLENIAN_FRUITS, constructor_page.get_fallenian_fruits_counter),
        ]:
            with allure.step(f"Добавление {name}"):
                constructor_page.drag_ingredient_to_constructor_by_locator(locator)
                assert counter_method() == 1, f"Счётчик {name} не равен 1"
        
        # === Шаг 7: Оформляем заказ ===
        with allure.step("Оформление заказа"):
            constructor_page.click_place_order_button()
        
        # === Шаг 8: Получаем номер заказа ===
        with allure.step("Получение номера заказа"):
            order_number = constructor_page.get_order_number_from_modal()
            allure.attach(order_number, name="Номер заказа", attachment_type=allure.attachment_type.TEXT)
        
        # === Шаг 9: Закрываем модалку ===
        with allure.step("Закрытие модального окна заказа"):
            constructor_page.close_order_modal()
    
    yield order_number