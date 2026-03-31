"""
Базовый класс для всех страниц сайта.
Содержит общие методы для:
- Навигации по страницам
- Поиска и взаимодействия с элементами
- Явных ожиданий (WebDriverWait)
- Работы с модальными окнами
- Allure-отчётности (шаги выполнения)
Все страницы наследуются от этого класса и получают его функциональность.
"""


import allure

from utils.config import AppConfig, TimeoutConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException


class BasePage:


    LOCATOR_MODAL_OVERLAY = (By.CSS_SELECTOR, ".Modal_modal_overlay__x2ZCr")
    BASE_URL = AppConfig.BASE_URL


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TimeoutConfig.EXPLICIT_WAIT_TIMEOUT)
        self.url = self.BASE_URL

    
    # МЕТОДЫ НАВИГАЦИИ

    @allure.step("Переход на страницу: {url}")
    # Открываем указанную страницу или базовый URL
    def open(self, url=None):
        target_url = url if url else self.url
        self.driver.get(target_url)
    
   
    @allure.step("Получение текущего URL")
    # Возвращаем текущий URL страницы
    def get_current_url(self):
        return self.driver.current_url 
    

    # МЕТОДЫ ПОИСКА ЭЛЕМЕНТОВ

    @allure.step("Поиск элемента: {locator}")
    # Находим одие элемент на странице с явным ожиданием
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    

    @allure.step("Поиск элементов: {locator}")
    # Находим все элементы на странице, соответствующие локатору
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)
    

    @allure.step("Проверка наличия элемента: {locator}")
    # Проверяем, присутствует ли элемент на странице
    def is_element_present(self, locator, timeout=TimeoutConfig.EXPLICIT_WAIT_TIMEOUT):
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
        

    @allure.step("Проверка видимости элемента: {locator}")
    # Проверяем, виден ли элемент на странице
    def is_element_visible(self, locator, timeout=TimeoutConfig.EXPLICIT_WAIT_TIMEOUT):

        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
        

    # МЕТОДЫ ВЗАИМОДЕЙСТВИЯ

    @allure.step("Клик по элементу: {locator}")
    # Кликаем по элементу с ожиданием кликабельности
    def click(self, locator):
            
        try:
            # Пробуем обычный клик с ожиданием
            element = self.wait_for_element_clickable(locator)
            element.click()
        except ElementClickInterceptedException:
            # Если элемент перекрыт — пробуем клик через JavaScript
            with allure.step("Элемент перекрыт, используем JavaScript клик"):
                element = self.find_element(locator)
                self.driver.execute_script("arguments[0].click();", element)
    

    @allure.step("Ввод текста в поле: {locator}")
    # Вводит текст в поле ввода
    def input_text(self, locator, text):

        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)
    

    @allure.step("Получение текста элемента: {locator}")
    # Получаем текст элемента 
    def get_text(self, locator):

        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text
    

    # МЕТОДЫ ОЖИДАНИЙ   

    @allure.step("Ожидание видимости элемента: {locator}")
    # Ждём пока элемент станет видимым
    def wait_for_element_visible(self, locator, timeout=TimeoutConfig.EXPLICIT_WAIT_TIMEOUT):

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    

    @allure.step("Ожидание кликабельности элемента: {locator}")
    # Ждём пока элемент станет кликабельным
    def wait_for_element_clickable(self, locator, timeout=TimeoutConfig.EXPLICIT_WAIT_TIMEOUT):

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    

    @allure.step("Ожидание исчезновения элемента: {locator}")
    # ждём пока элемент исчезнет со страницы
    def wait_for_element_disappear(self, locator, timeout=TimeoutConfig.EXPLICIT_WAIT_TIMEOUT):

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    

    # МЕТОДЫ ДЛЯ РАБОТЫ С DRIVER
    # Эти методы инкапсулируют прямые вызовы self.driver
    # Дочерние классы должны использовать их вместо прямого доступа к driver
    
    @allure.step("Возвращает экземпляр драйвера")
    def _get_driver(self):
        return self.driver
    
    @allure.step("Создаёт и возвращает WebDriverWait")
    def _get_wait(self, timeout=None, poll_frequency=1):
        if timeout is None:
            timeout = TimeoutConfig.EXPLICIT_WAIT_TIMEOUT
        return WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
    
    @allure.step("Выполняет JavaScript код")
    def _execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)
    
    @allure.step("Возвращает возможности браузера")
    def _get_capabilities(self):
        return self.driver.capabilities
    
    @allure.step("Возвращает имя браузера")
    def _get_browser_name(self):
        return self.driver.capabilities.get('browserName', '').lower()
    
    @allure.step("Создаёт и возвращает ActionChains")
    def _create_action_chains(self):
        from selenium.webdriver.common.action_chains import ActionChains
        return ActionChains(self.driver)
    
    @allure.step("Очищает все cookies")
    def delete_all_cookies(self):
        self.driver.delete_all_cookies()