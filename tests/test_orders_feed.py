"""
Тесты для проверки функциональности ленты заказов.
Тестируемая функциональность:
1. При создании заказа счётчик «Выполнено за всё время» увеличивается
2. При создании заказа счётчик «Выполнено за сегодня» увеличивается
3. После оформления заказа номер появляется в разделе «В работе»
Все тесты ТРЕБУЮТ авторизации (используют фикстуру login_user).
"""

import allure  
import pytest  


@allure.feature("Лента заказов")
@allure.story("Счётчики выполненных заказов")
class TestOrderCounters:

    
    @allure.title("Счётчик «Выполнено за всё время» увеличивается после заказа")
    def test_completed_all_time_counter_increases(self, login_user, constructor_page, orders_feed_page):

        # Переходим на ленту заказов и сохраняем старое значение счётчика
        with allure.step("Переход на ленту заказов и получение текущего счётчика"):
            orders_feed_page.open_orders_feed_page()
            old_counter = orders_feed_page.get_completed_all_time_count()
            allure.attach(f"Старое значение: {old_counter}", name="Счётчик до заказа", attachment_type=allure.attachment_type.TEXT)
        
        # Переходим в конструктор и создаём заказ
        with allure.step("Переход в конструктор и создание заказа"):
            constructor_page.open_constructor_page()
            # Создаём заказ через фикстуру create_order (вызываем явно)
            order_number = constructor_page.create_order()
            allure.attach(f"Номер заказа: {order_number}", name="Созданный заказ", attachment_type=allure.attachment_type.TEXT)
        
        # Возвращаемся на ленту и проверяем увеличение счётчика
        with allure.step("Возврат на ленту заказов и проверка счётчика"):
            orders_feed_page.open_orders_feed_page()
            orders_feed_page.wait_for_all_time_counter_increase(old_counter, timeout=15)
            new_counter = orders_feed_page.get_completed_all_time_count()
            allure.attach(f"Новое значение: {new_counter}", name="Счётчик после заказа", attachment_type=allure.attachment_type.TEXT)
            
            assert int(new_counter) > int(old_counter), (
                f"Счётчик «Выполнено за всё время» не увеличился. Было: {old_counter}, стало: {new_counter}"
            )
    

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается после заказа")
    def test_completed_today_counter_increases(self, login_user, constructor_page, orders_feed_page):

        # Переходим на ленту заказов и сохраняем старое значение счётчика
        with allure.step("Переход на ленту заказов и получение текущего счётчика"):
            orders_feed_page.open_orders_feed_page()
            old_counter = orders_feed_page.get_completed_today_count()
            allure.attach(f"Старое значение: {old_counter}", name="Счётчик до заказа", attachment_type=allure.attachment_type.TEXT)
        
        # Переходим в конструктор и создаём заказ
        with allure.step("Переход в конструктор и создание заказа"):
            constructor_page.open_constructor_page()
            order_number = constructor_page.create_order()
            allure.attach(f"Номер заказа: {order_number}", name="Созданный заказ", attachment_type=allure.attachment_type.TEXT)
        
        # Возвращаемся на ленту и проверяем увеличение счётчика
        with allure.step("Возврат на ленту заказов и проверка счётчика"):
            orders_feed_page.open_orders_feed_page()
            orders_feed_page.wait_for_today_counter_increase(old_counter, timeout=15)
            new_counter = orders_feed_page.get_completed_today_count()
            allure.attach(f"Новое значение: {new_counter}", name="Счётчик после заказа", attachment_type=allure.attachment_type.TEXT)
            
            assert int(new_counter) > int(old_counter), (
                f"Счётчик «Выполнено за сегодня» не увеличился. Было: {old_counter}, стало: {new_counter}"
            )


@allure.feature("Лента заказов")
@allure.story("Номер заказа в разделе «В работе»")
class TestOrderInWork:

    
    @allure.title("Номер заказа появляется в разделе «В работе» после оформления")
    def test_order_number_appears_in_work_section(self, login_user, constructor_page, orders_feed_page):

        # Переходим в конструктор и создаём заказ
        with allure.step("Переход в конструктор и создание заказа"):
            constructor_page.open_constructor_page()
            order_number = constructor_page.create_order()
            allure.attach(f"Номер заказа: {order_number}", name="Созданный заказ", attachment_type=allure.attachment_type.TEXT)

        # СРАЗУ переходим на ленту заказов (без задержек!)
        with allure.step("Переход на ленту заказов"):
            orders_feed_page.open_orders_feed_page()  # ← Сразу после create_order()

        # Проверяем появление номера в разделе «В работе»
        with allure.step("Проверка появления номера в разделе «В работе»"):
            order_found = orders_feed_page.wait_for_order_in_work(order_number, timeout=30)  # ← 30 секунд
            assert order_found, f"Номер заказа {order_number} не найден в разделе «В работе»"
