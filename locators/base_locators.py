""" Универсальные локаторы """

from selenium.webdriver.common.by import By

# --- Навигация (Header) ---

# Кнопка «Конструктор» в хедере (активная страница)
LOCATOR_CONSTRUCTOR_TAB = (By.LINK_TEXT, "Конструктор")

# Кнопка «Лента Заказов» в хедере (переход на ленту заказов)
LOCATOR_ORDERS_FEED_TAB = (By.LINK_TEXT, "Лента Заказов")

# Кнопка «Личный Кабинет» в хедере
LOCATOR_PERSONAL_CABINET_BTN = (By.CSS_SELECTOR, "a[href='/account']")


# --- Модальное окно ингредиента ---

# Контейнер модального окна
LOCATOR_MODAL_CONTAINER = (By.CSS_SELECTOR, ".Modal_modal__container__Wo2l_")

# Заголовок модального окна
LOCATOR_MODAL_TITLE = (By.CSS_SELECTOR, ".Modal_modal__title__2L34m")

# Кнопка закрытия модального окна (крестик)
LOCATOR_MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, 'button.Modal_modal__close__TnseK')

# Находит номер заказа в модальном окне после оформления заказа
LOCATOR_ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")