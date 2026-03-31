""" Локаторы для ConstructorPage """

from selenium.webdriver.common.by import By


# --- Ингредиенты (карточки) ---

# Карточка ингредиента (общий селектор для всех ингредиентов)
LOCATOR_INGREDIENT_CARD = (By.CSS_SELECTOR, "a[draggable='true']")

# Счётчик ингредиента (число внутри карточки: 0, 1, 2...)
LOCATOR_INGREDIENT_COUNTER = (By.XPATH, "//div[contains(@class, 'counter_counter')]/p")


# Тестовые данные для заказа

# === Краторная булка ===
LOCATOR_KRATOR_BUN = (By.XPATH, "//p[text()='Краторная булка N-200i']")
LOCATOR_KRATOR_BUN_COUNTER = (By.XPATH, "//p[text()='Краторная булка N-200i']/ancestor::a//div[contains(@class, 'counter_counter')]/p")

# === Соус Spicy-X ===
LOCATOR_SPICY_SAUCE = (By.XPATH, "//p[text()='Соус Spicy-X']")
LOCATOR_SPICY_SAUCE_COUNTER = (By.XPATH, "//p[text()='Соус Spicy-X']/ancestor::a//div[contains(@class, 'counter_counter')]/p")

# === Говяжий метеорит ===
LOCATOR_BEEF_METEORITE = (By.XPATH, "//p[text()='Говяжий метеорит (отбивная)']")
LOCATOR_BEEF_METEORITE_COUNTER = (By.XPATH, "//p[text()='Говяжий метеорит (отбивная)']/ancestor::a//div[contains(@class, 'counter_counter')]/p")

# === Хрустящие кольца ===
LOCATOR_CRISPY_RINGS = (By.XPATH, "//p[text()='Хрустящие минеральные кольца']")
LOCATOR_CRISPY_RINGS_COUNTER = (By.XPATH, "//p[text()='Хрустящие минеральные кольца']/ancestor::a//div[contains(@class, 'counter_counter')]/p")

# === Плоды Фалленианского дерева ===
LOCATOR_FALLENIAN_FRUITS = (By.XPATH, "//p[text()='Плоды Фалленианского дерева']")
LOCATOR_FALLENIAN_FRUITS_COUNTER = (By.XPATH, "//p[text()='Плоды Фалленианского дерева']/ancestor::a//div[contains(@class, 'counter_counter')]/p")
