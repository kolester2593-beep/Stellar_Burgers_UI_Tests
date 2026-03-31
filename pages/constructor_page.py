"""
Класс для страницы конструктора бургеров.
Этот класс инкапсулирует всю логику работы со страницей конструктора:
- Навигация по табам (Булки, Соусы, Начинки)
- Работа с карточками ингредиентов
- Drag-and-Drop ингредиентов в конструктор
- Проверка счётчиков ингредиентов
- Оформление заказа
- Работа с модальными окнами ингредиентов
"""

from pages.base_page import BasePage
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException
)

import allure

from locators.base_locators import (
    LOCATOR_MODAL_CLOSE_BUTTON,
    LOCATOR_ORDER_NUMBER
)

from locators.main_locators import (
    LOCATOR_BUNS_TAB,
    LOCATOR_SAUCE_TAB,
    LOCATOR_FILLING_TAB,
    LOCATOR_INGREDIENT_CARD,
    LOCATOR_BUTTON_PLACE_ORDER,
    LOCATOR_CONSTRUCTOR_DROP_ZONE,
)

from locators.constructor_locators import (
    LOCATOR_INGREDIENT_CARD,
    LOCATOR_INGREDIENT_COUNTER,
    LOCATOR_KRATOR_BUN,
    LOCATOR_KRATOR_BUN_COUNTER,
    LOCATOR_SPICY_SAUCE,
    LOCATOR_SPICY_SAUCE_COUNTER,
    LOCATOR_BEEF_METEORITE,
    LOCATOR_BEEF_METEORITE_COUNTER,
    LOCATOR_CRISPY_RINGS_COUNTER,
    LOCATOR_FALLENIAN_FRUITS_COUNTER,
)



class ConstructorPage(BasePage):
    

    # МЕТОДЫ НАВИГАЦИИ

    @allure.step("Переход на страницу конструктора")
    def open_constructor_page(self):
        self.open(self.BASE_URL)
    

    # МЕТОДЫ РАБОТЫ С ТАБАМИ ИНГРЕДИЕНТОВ

    @allure.step("Переключение на таб «Булки»")
    def switch_to_buns_tab(self):
        self.click(LOCATOR_BUNS_TAB)
    

    @allure.step("Переключение на таб «Соусы»")
    def switch_to_sauce_tab(self):
        self.click(LOCATOR_SAUCE_TAB) 

    
    @allure.step("Переключение на таб «Начинки»")
    def switch_to_filling_tab(self):
        self.click(LOCATOR_FILLING_TAB) 
    

    # МЕТОДЫ РАБОТЫ С ИНГРЕДИЕНТАМИ
    
    @allure.step("Получение списка всех ингредиентов")
    def get_all_ingredients(self):
        return self.find_elements(LOCATOR_INGREDIENT_CARD)
    
    
    @allure.step("Получение ингредиента по индексу: {index}")
    def get_ingredient_by_index(self, index):
        ingredients = self.get_all_ingredients()
        return ingredients[index]
    
    
    @allure.step("Получение счётчика ингредиента по индексу: {index}")
    def get_ingredient_counter(self, index=0):
        ingredient = self.get_ingredient_by_index(index)
        counter = ingredient.find_element(*LOCATOR_INGREDIENT_COUNTER)
        return counter.text 
    
    
    # МЕТОДЫ DRAG-AND-DROP
    
    @allure.step("Drag-and-Drop ингредиента в конструктор: индекс {index}")
    def drag_ingredient_to_constructor(self, index=0):
        # Находим ингредиент
        ingredient = self.get_ingredient_by_index(index)
        # Находим зону конструктора
        constructor_zone = self.wait_for_element_visible(LOCATOR_CONSTRUCTOR_DROP_ZONE)
        # Создаём ActionChains
        actions = self._create_action_chains()
        # Выполняем перетаскивание
        actions.click_and_hold(ingredient)
        actions.move_to_element(constructor_zone)
        actions.release()
        actions.perform()
    

    @allure.step("Drag-and-Drop ингредиента через JavaScript: индекс {index}")
    def drag_ingredient_to_constructor_js(self, index=0):
        # Находим ингредиент и зону конструктора
        ingredient = self.get_ingredient_by_index(index)
        constructor_zone = self.wait_for_element_visible(LOCATOR_CONSTRUCTOR_DROP_ZONE)
        # Выполняем JavaScript для эмуляции drag-and-drop
        self._execute_script("""
            function createDragEvent(name) {
                const event = new Event(name, { bubbles: true });
                event.dataTransfer = { 
                    getData: () => '', 
                    setData: () => {},
                    items: { add: () => {} }
                };
                return event;
            }
            
            // Эмулируем последовательность событий drag-and-drop
            arguments[0].dispatchEvent(createDragEvent('dragstart'));
            arguments[1].dispatchEvent(createDragEvent('dragover'));
            arguments[1].dispatchEvent(new Event('drop', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('dragend', { bubbles: true }));
        """, ingredient, constructor_zone)
        
    
    # МЕТОДЫ ПРОВЕРКИ СЧЁТЧИКОВ
    
    @allure.step("Проверка увеличения счётчика ингредиента: индекс {index}")
    def wait_for_counter_increase(self, index=0, old_value="0", timeout=10):
        # Используем переданный timeout вместо TimeoutConfig.EXPLICIT_WAIT_TIMEOUT
        wait = self._get_wait(timeout)
    
        def counter_changed(driver):
            current_value = self.get_ingredient_counter(index)
            return current_value != old_value
        
        return wait.until(counter_changed) 
    
    @allure.step("Получение текущего значения счётчика: индекс {index}")
    def get_counter_value(self, index=0):
        counter_text = self.get_ingredient_counter(index)
        return int(counter_text)

    @allure.step("Ожидание значения счётчика по названию: {ingredient_name} = {expected_value}")
    def wait_for_counter_value_by_name(self, ingredient_name, expected_value, timeout=10):
        wait = self._get_wait(timeout)
        
        def counter_equals(driver):
            current = self.get_counter_by_name(ingredient_name)
            return current == expected_value
        
        return wait.until(counter_equals)


    # МЕТОДЫ РАБОТЫ С МОДАЛЬНЫМИ ОКНАМИ

    @allure.step("Получение номера заказа из модального окна")
    def get_order_number_from_modal(self, timeout=60):
        wait = self._get_wait(timeout, poll_frequency=1)
        
        # Условие с обработкой исключений
        def order_number_is_valid(driver):
            try:
                # Находим элемент
                order_element = driver.find_element(*LOCATOR_ORDER_NUMBER)
                order_number = order_element.text.strip()
                
                # Проверяем, что номер состоит ровно из 6 цифр и не равен "9999"
                if len(order_number) == 6 and order_number.isdigit() and order_number != "9999":
                    return True
                else:
                    return False
                    
            except StaleElementReferenceException:
                return False
            except NoSuchElementException:
                # Элемент ещё не появился в DOM
                return False
            except TimeoutException:
                # Превышено время ожидания
                return False
        
        # Ждём валидного номера заказа
        wait.until(order_number_is_valid)
        # Возвращаем номер заказа (теперь он точно валидный)
        order_element = self.find_element(LOCATOR_ORDER_NUMBER)
        return order_element.text.strip()

    
    # МЕТОДЫ ДЛЯ ПРОВЕРКИ СЧЁТЧИКОВ ПО ИМЕНИ
    
    @allure.step("Получение счётчика булки Краторная")
    def get_krator_bun_counter(self):
        return int(self.get_text(LOCATOR_KRATOR_BUN_COUNTER))
    
    @allure.step("Получение счётчика соуса Spicy-X")
    def get_spicy_sauce_counter(self):
        return int(self.get_text(LOCATOR_SPICY_SAUCE_COUNTER))
    
    @allure.step("Получение счётчика Говяжьего метеорита")
    def get_beef_meteorite_counter(self):
        return int(self.get_text(LOCATOR_BEEF_METEORITE_COUNTER))
    
    @allure.step("Получение счётчика Хрустящих колец")
    def get_crispy_rings_counter(self):
        return int(self.get_text(LOCATOR_CRISPY_RINGS_COUNTER))
    
    @allure.step("Получение счётчика Плодов Фалленианского дерева")
    def get_fallenian_fruits_counter(self):
        return int(self.get_text(LOCATOR_FALLENIAN_FRUITS_COUNTER))
    

    # МЕТОДЫ ДЛЯ DRAG-AND-DROP ПО ЛОКАТОРУ
    
    @allure.step("Drag-and-Drop ингредиента по локатору в конструктор")
    def drag_ingredient_to_constructor_by_locator(self, ingredient_locator, timeout=10):
        ingredient = self.wait_for_element_clickable(ingredient_locator, timeout=timeout)
        drop_zone = self.wait_for_element_visible(LOCATOR_CONSTRUCTOR_DROP_ZONE)
        
        # Определяем браузер и выбираем метод
        browser_name = self._get_browser_name()
        
        if browser_name == 'firefox':
            # Для Firefox используем JavaScript
            self._execute_script("""
                function createDragEvent(name) {
                    const event = new Event(name, { bubbles: true });
                    event.dataTransfer = { 
                        getData: () => '', 
                        setData: () => {},
                        items: { add: () => {} }
                    };
                    return event;
                }
                arguments[0].dispatchEvent(createDragEvent('dragstart'));
                arguments[1].dispatchEvent(createDragEvent('dragover'));
                arguments[1].dispatchEvent(new Event('drop', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('dragend', { bubbles: true }));
            """, ingredient, drop_zone)
        else:
            
            actions = self._create_action_chains()
            actions.click_and_hold(ingredient)
            actions.move_to_element(drop_zone)
            actions.release()
            actions.perform()
        

    # МЕТОДЫ ДЛЯ ОФОРМЛЕНИЯ ЗАКАЗА
    
    @allure.step("Клик по кнопке «Оформить заказ»")
    def click_place_order_button(self):
        self.click(LOCATOR_BUTTON_PLACE_ORDER)
    
    
    @allure.step("Закрытие модального окна заказа")
    def close_order_modal(self):
        self.click(LOCATOR_MODAL_CLOSE_BUTTON)


    # МЕТОДЫ ДЛЯ СОЗДАНИЯ ЗАКАЗА 

    @allure.step("Создание тестового заказа")
    def create_order(self):

        # Добавляем булку
        self.drag_ingredient_to_constructor_by_locator(LOCATOR_KRATOR_BUN)
        # Добавляем соус
        self.drag_ingredient_to_constructor_by_locator(LOCATOR_SPICY_SAUCE)
        # Переключаемся на начинки
        self.click(LOCATOR_FILLING_TAB)
        # Добавляем начинку
        self.drag_ingredient_to_constructor_by_locator(LOCATOR_BEEF_METEORITE)
        # Оформляем заказ
        self.click_place_order_button()
        # Получаем номер заказа
        order_number = self.get_order_number_from_modal(timeout=30)
        # Закрываем модальное окно
        self.close_order_modal()
        
        return order_number