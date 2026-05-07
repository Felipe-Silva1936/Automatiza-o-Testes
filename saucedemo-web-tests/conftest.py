import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from utils.driver_factory import DriverFactory
from pages import (
    LoginPage,
    InventoryPage,
    CartPage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutCompletePage,
)
from config.settings import settings

# ──────────────────────────────────────────────────────────────────────────────
# Driver lifecycle
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver() -> WebDriver:
    """Fresh WebDriver per test, guaranteed teardown."""
    _driver = DriverFactory.create_driver()
    yield _driver
    _driver.quit()

# ──────────────────────────────────────────────────────────────────────────────
# Page Object fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def login_page(driver: WebDriver) -> LoginPage:
    return LoginPage(driver)

@pytest.fixture
def inventory_page(driver: WebDriver) -> InventoryPage:
    return InventoryPage(driver)

@pytest.fixture
def cart_page(driver: WebDriver) -> CartPage:
    return CartPage(driver)

@pytest.fixture
def checkout_info_page(driver: WebDriver) -> CheckoutInfoPage:
    return CheckoutInfoPage(driver)

@pytest.fixture
def checkout_overview_page(driver: WebDriver) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(driver)

@pytest.fixture
def checkout_complete_page(driver: WebDriver) -> CheckoutCompletePage:
    return CheckoutCompletePage(driver)

# ──────────────────────────────────────────────────────────────────────────────
# Authenticated session fixture
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def authenticated_inventory(driver: WebDriver) -> InventoryPage:
    """
    Starts every test already logged in and on the inventory page.
    Avoids repeating the login flow in tests that don't cover auth.
    """
    login = LoginPage(driver)
    login.open()
    login.login(settings.STANDARD_USER, settings.PASSWORD)
    # Aguarda navegação para o inventário antes de retornar
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(driver, settings.IMPLICIT_WAIT).until(
        EC.url_contains("inventory"),
        message="Inventory page did not load after login"
    )
    return InventoryPage(driver)

@pytest.fixture
def cart_with_one_item(authenticated_inventory: InventoryPage) -> CartPage:
    """
    Adds one item to cart and navigates to cart page.
    Used as precondition for cart and checkout tests.
    """
    authenticated_inventory.add_first_item_to_cart()
    authenticated_inventory.go_to_cart()
    # go_to_cart já aguarda url_contains("cart")
    return CartPage(authenticated_inventory._driver)

@pytest.fixture
def checkout_info_ready(cart_with_one_item: CartPage) -> CheckoutInfoPage:
    """Proceeds to checkout step 1 with one item already in cart."""
    cart_with_one_item.go_to_checkout()
    # go_to_checkout já aguarda url_contains("checkout-step-one")
    return CheckoutInfoPage(cart_with_one_item._driver)

@pytest.fixture
def checkout_overview_ready(checkout_info_ready: CheckoutInfoPage) -> CheckoutOverviewPage:
    """Proceeds to checkout step 2 (overview) with valid shipping info filled."""
    checkout_info_ready.submit("João", "Silva", "01310-100")
    # Aguarda navegação para a overview antes de retornar
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    WebDriverWait(checkout_info_ready._driver, settings.IMPLICIT_WAIT).until(
        EC.url_contains("checkout-step-two"),
        message="Checkout overview did not load after submitting info"
    )
    return CheckoutOverviewPage(checkout_info_ready._driver)