""" Локаторы для MainPage """

from selenium.webdriver.common.by import By

# --- Заголовок страницы ---

# Заголовок «Соберите бургер»
LOCATOR_CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")

# --- Табы ингредиентов ---

# Таб «Булки» (переключение на булки)
LOCATOR_BUNS_TAB = (By.XPATH, "//span[text()='Булки']")

# Таб «Соусы» (переключение на соусы)
LOCATOR_SAUCE_TAB = (By.XPATH, "//span[text()='Соусы']")

# Таб «Начинки» (переключение на начинки)
LOCATOR_FILLING_TAB = (By.XPATH, "//span[text()='Начинки']")

# Активный таб (имеет класс tab_tab_type_current__2BEPc)
LOCATOR_ACTIVE_TAB = (By.CSS_SELECTOR, ".tab_tab_type_current__2BEPc")

# --- Ингредиенты (карточки) ---

# Карточка ингредиента (общий селектор для всех ингредиентов)
LOCATOR_INGREDIENT_CARD = (By.CSS_SELECTOR, ".BurgerIngredient_ingredient__1TVf6")

# Название ингредиента (текст под картинкой)
LOCATOR_INGREDIENT_NAME = (By.CSS_SELECTOR, ".BurgerIngredient_ingredient__text__yp3dH")

#Находит текстовое значение счётчика (цифру)
LOCATOR_INGREDIENT_COUNTER = (By.CSS_SELECTOR, ".counter_counter__num__3nue1")


# --- Конструктор (корзина) ---

# Кнопка «Войти в аккаунт» (в конструкторе, когда не авторизован)
LOCATOR_LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")

# Кнопка «Оформить заказ» (в конструкторе, когда авторизован)
LOCATOR_BUTTON_PLACE_ORDER = (By.XPATH, "//button[text()='Оформить заказ']")

# Зона конструктора (куда перетаскиваем)
LOCATOR_CONSTRUCTOR_DROP_ZONE = (By.CSS_SELECTOR, 'section.BurgerConstructor_basket__29Cd7')