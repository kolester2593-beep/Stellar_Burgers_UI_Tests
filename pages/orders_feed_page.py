"""
Класс для страницы «Лента заказов».
Этот класс инкапсулирует всю логику работы со страницей ленты заказов:
- Проверка заголовка страницы
- Получение списка заказов
- Получение счётчиков «Выполнено за все время» и «Выполнено за сегодня»
- Получение номеров заказов из раздела «В работе»
- Проверка появления нового заказа после оформления
"""

import allure

from pages.base_page import BasePage
from selenium.common.exceptions import (
        NoSuchElementException,
        StaleElementReferenceException,
        TimeoutException
)


from locators.base_locators import (
    LOCATOR_CONSTRUCTOR_TAB,
    LOCATOR_ORDER_NUMBER
)


from locators.orders_feed_locators import (
    LOCATOR_PAGE_HEADER,
    LOCATOR_ORDER_CARD,
    LOCATOR_COMPLETED_ALL_TIME_COUNTER,
    LOCATOR_COMPLETED_TODAY_COUNTER,
    LOCATOR_READY_LABEL,
    LOCATOR_IN_WORK_LABEL,
    LOCATOR_IN_WORK_ORDER_NUMBER,
    LOCATOR_READY_ORDER_NUMBER,
    LOCATOR_ALL_ORDERS_READY_MESSAGE,
)



class OrdersFeedPage(BasePage):
    

    # МЕТОДЫ НАВИГАЦИИ
    
    @allure.step("Открытие страницы ленты заказов")
    def open_orders_feed_page(self):
        self.open(f"{self.BASE_URL}feed")
    
    @allure.step("Переход на страницу конструктора")
    def go_to_constructor(self):
        self.click(LOCATOR_CONSTRUCTOR_TAB)
    
    @allure.step("Проверка заголовка страницы ленты заказов")
    def is_page_header_visible(self):
        return self.is_element_visible(LOCATOR_PAGE_HEADER)
    

    # МЕТОДЫ ПОЛУЧЕНИЯ СЧЁТЧИКОВ
    
    @allure.step("Получение значения счётчика «Выполнено за все время»")
    def get_completed_all_time_count(self):
        return self.get_text(LOCATOR_COMPLETED_ALL_TIME_COUNTER)
    
    @allure.step("Получение значения счётчика «Выполнено за сегодня»")
    def get_completed_today_count(self):
        return self.get_text(LOCATOR_COMPLETED_TODAY_COUNTER)
    
    @allure.step("Получение значений обоих счётчиков")
    def get_both_counters(self):
        all_time = self.get_completed_all_time_count()
        today = self.get_completed_today_count()
        return all_time, today
    

    # МЕТОДЫ ПОЛУЧЕНИЯ ЗАКАЗОВ
    
    @allure.step("Получение списка всех карточек заказов")
    def get_all_order_cards(self):
        return self.find_elements(LOCATOR_ORDER_CARD)
    
    @allure.step("Получение количества заказов на странице")
    def get_orders_count(self):
        return len(self.get_all_order_cards())
    
    @allure.step("Получение первого номера заказа из списка")
    def get_first_order_number(self):
        order_cards = self.get_all_order_cards()
        if order_cards:
            # Находим номер внутри первой карточки
            number_element = order_cards[0].find_element(LOCATOR_ORDER_NUMBER)
            # Убираем символ # если он есть
            return number_element.text.replace("#", "")
        
        return ""
    
    @allure.step("Получение списка номеров заказов в работе")
    def get_in_work_order_numbers(self):
        # Находим все элементы номеров в разделе «В работе»
        in_work_elements = self.find_elements(LOCATOR_IN_WORK_ORDER_NUMBER) 
        # Извлекаем текст из каждого элемента
        order_numbers = []
        for element in in_work_elements:
            order_numbers.append(element.text)
        return order_numbers
    
    @allure.step("Получение списка номеров готовых заказов")
    def get_ready_order_numbers(self):
        ready_elements = self.find_elements(LOCATOR_READY_ORDER_NUMBER)
        order_numbers = []
        for element in ready_elements:
            order_numbers.append(element.text)
        
        return order_numbers
    

    # МЕТОДЫ ПРОВЕРКИ ПОЯВЛЕНИЯ ЗАКАЗА
    
    @allure.step("Проверка появления номера заказа в разделе «В работе»")
    def wait_for_order_in_work(self, order_number, timeout=30): 
        wait = self._get_wait(timeout, poll_frequency=1)
        
        def order_appeared(driver):
            try:
                order_numbers = self.get_in_work_order_numbers()
                
                # Нормализуем оба номера для сравнения (убираем ведущие нули)
                target_number = order_number.lstrip('0')
                found_numbers = [num.lstrip('0') for num in order_numbers]
                
                found = target_number in found_numbers

                return found
            except (NoSuchElementException, StaleElementReferenceException):
                return False
            except TimeoutException:
                return False
        
        return wait.until(order_appeared)


    @allure.step("Проверка увеличения счётчика «Выполнено за все время»")
    def wait_for_all_time_counter_increase(self, old_value, timeout=10):
        wait = self._get_wait(timeout)
        
        def counter_changed(driver):
            current_value = self.get_completed_all_time_count()
            return current_value != old_value
        
        return wait.until(counter_changed)
    
    @allure.step("Проверка увеличения счётчика «Выполнено за сегодня»")
    def wait_for_today_counter_increase(self, old_value, timeout=10):
        wait = self._get_wait(timeout)
        
        def counter_changed(driver):
            current_value = self.get_completed_today_count()
            return current_value != old_value
        
        return wait.until(counter_changed)
    

    # МЕТОДЫ ПРОВЕРКИ СОСТОЯНИЯ СТРАНИЦЫ
    
    @allure.step("Проверка видимости раздела «В работе»")
    def is_in_work_section_visible(self):
        return self.is_element_visible(LOCATOR_IN_WORK_LABEL)
    
    @allure.step("Проверка видимости раздела «Готовы»")
    def is_ready_section_visible(self):
        return self.is_element_visible(LOCATOR_READY_LABEL)
    
    @allure.step("Проверка наличия заказов в разделе «В работе»")
    def has_orders_in_work(self):
        order_numbers = self.get_in_work_order_numbers()
        return len(order_numbers) > 0
    
    @allure.step("Проверка сообщения «Все текущие заказы готовы»")
    def is_all_orders_ready_message_visible(self):
        return self.is_element_present(LOCATOR_ALL_ORDERS_READY_MESSAGE, timeout=3)
    

    # КОМПЛЕКСНЫЕ МЕТОДЫ
    
    @allure.step("Получение состояния счётчиков перед заказом")
    def get_counters_before_order(self):
        return {
            'all_time': self.get_completed_all_time_count(),
            'today': self.get_completed_today_count()
        }
    
    @allure.step("Проверка обновления всех счётчиков после заказа")
    def verify_counters_updated(self, before_values):
        wait = self._get_wait(10)

        # Ждём увеличения счётчика «За все время»
        def all_time_changed(driver):
            current = self.get_completed_all_time_count()
            return current != before_values['all_time']
        
        # Ждём увеличения счётчика «За сегодня»
        def today_changed(driver):
            current = self.get_completed_today_count()
            return current != before_values['today']
        
        # Ждём оба изменения
        all_time_updated = wait.until(all_time_changed)
        today_updated = wait.until(today_changed)
        
        return all_time_updated and today_updated