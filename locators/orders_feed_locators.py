""" Локаторы для OrdersFeedPage """

from selenium.webdriver.common.by import By

    
# --- Заголовок и навигация ---

# Заголовок страницы «Лента заказов»
LOCATOR_PAGE_HEADER = (By.XPATH, "//h1[text()='Лента заказов']")


# --- Список заказов ---

# Карточка заказа в списке
LOCATOR_ORDER_CARD = (By.CSS_SELECTOR, ".OrderHistory_listItem__2x95r")


# --- Счётчики выполненных заказов ---

# Значение счётчика «Выполнено за все время»
LOCATOR_COMPLETED_ALL_TIME_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")

# Значение счётчика «Выполнено за сегодня»
LOCATOR_COMPLETED_TODAY_COUNTER = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")


# --- Статусы заказов (Готовы / В работе) ---

# Текст «Готовы:»
LOCATOR_READY_LABEL = (By.XPATH, "//p[text()='Готовы:']")

# Текст «В работе:»
LOCATOR_IN_WORK_LABEL = (By.XPATH, "//p[text()='В работе:']")

# Номер заказа в разделе «В работе»
LOCATOR_IN_WORK_ORDER_NUMBER = (By.CSS_SELECTOR, ".OrderFeed_orderList__cBvyi .text_type_digits-default")

# Номер заказа в разделе «Готовы»
LOCATOR_READY_ORDER_NUMBER = (By.CSS_SELECTOR, ".OrderFeed_orderListReady__1YFem .text_type_digits-default")

# Сообщение «Все текущие заказы готовы!»
LOCATOR_ALL_ORDERS_READY_MESSAGE = (By.XPATH, "//li[text()='Все текущие заказы готовы!']")