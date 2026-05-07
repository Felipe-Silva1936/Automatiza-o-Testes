"""
Test Suite: Checkout — End-to-End Purchase Flow
Covers the full functional path:
  Login → Add to Cart → Cart → Checkout Info → Overview → Confirmation

Also covers: form validation, price calculation, navigation cancellation.
"""
import pytest
from pages import (
    LoginPage,
    InventoryPage,
    CartPage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutCompletePage,
)
from utils.assertions import WebAssertions
from config.settings import settings

SAUCE_LABS_BACKPACK = "Sauce Labs Backpack"
SAUCE_LABS_BIKE_LIGHT = "Sauce Labs Bike Light"


# ──────────────────────────────────────────────────────────────────────────────
# Full E2E
# ──────────────────────────────────────────────────────────────────────────────

class TestFullPurchaseFlow:
    """Complete happy-path: login → add product → cart → checkout → confirmation."""

    def test_complete_purchase_flow(self, driver):
        """E2E: standard_user realiza compra completa do login à confirmação."""
        # Step 1 — Login
        login = LoginPage(driver)
        login.open()
        login.login(settings.STANDARD_USER, settings.PASSWORD)
        WebAssertions.assert_url_contains(driver, "inventory")

        # Step 2 — Adiciona produto ao carrinho
        inventory = InventoryPage(driver)
        assert inventory.get_page_title() == "Products"
        inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)

        # Step 3 — Verifica item no carrinho
        inventory.go_to_cart()
        cart = CartPage(driver)
        WebAssertions.assert_url_contains(driver, "cart")
        assert SAUCE_LABS_BACKPACK in cart.get_item_names()
        WebAssertions.assert_items_count(cart.get_item_count(), 1, "cart items")

        # Step 4 — Checkout info
        cart.go_to_checkout()
        checkout_info = CheckoutInfoPage(driver)
        WebAssertions.assert_url_contains(driver, "checkout-step-one")
        checkout_info.submit("João", "Silva", "01310-100")

        # Step 5 — Overview
        overview = CheckoutOverviewPage(driver)
        WebAssertions.assert_url_contains(driver, "checkout-step-two")
        assert SAUCE_LABS_BACKPACK in overview.get_item_names()
        subtotal = overview.get_subtotal_value()
        tax      = overview.get_tax_value()
        total    = overview.get_total_value()
        assert round(subtotal + tax, 2) == total

        # Step 6 — Confirmação
        overview.click_finish()
        complete = CheckoutCompletePage(driver)
        WebAssertions.assert_url_contains(driver, "checkout-complete")
        assert complete.is_order_confirmed()

    def test_complete_purchase_with_multiple_items(self, driver):
        """E2E com dois itens."""
        login = LoginPage(driver)
        login.open()
        login.login(settings.STANDARD_USER, settings.PASSWORD)
        WebAssertions.assert_url_contains(driver, "inventory")

        inventory = InventoryPage(driver)
        inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        inventory.add_item_to_cart_by_name(SAUCE_LABS_BIKE_LIGHT)

        inventory.go_to_cart()
        cart = CartPage(driver)
        WebAssertions.assert_items_count(cart.get_item_count(), 2, "cart items")

        cart.go_to_checkout()
        CheckoutInfoPage(driver).submit("Ana", "Costa", "20040-020")

        overview = CheckoutOverviewPage(driver)
        WebAssertions.assert_items_count(overview.get_item_count(), 2, "overview items")

        overview.click_finish()
        assert CheckoutCompletePage(driver).is_order_confirmed()


# ──────────────────────────────────────────────────────────────────────────────
# Checkout Info — form validation
# ──────────────────────────────────────────────────────────────────────────────

class TestCheckoutInfoValidation:
    """Shipping info form validation."""

    def test_missing_first_name_shows_error(self, checkout_info_ready: CheckoutInfoPage):
        checkout_info_ready.fill_info("", "Silva", "01310-100")
        checkout_info_ready.click_continue()

        assert checkout_info_ready.is_error_visible()
        assert "First Name is required" in checkout_info_ready.get_error_message()

    def test_missing_last_name_shows_error(self, checkout_info_ready: CheckoutInfoPage):
        checkout_info_ready.fill_info("João", "", "01310-100")
        checkout_info_ready.click_continue()

        assert checkout_info_ready.is_error_visible()
        assert "Last Name is required" in checkout_info_ready.get_error_message()

    def test_missing_postal_code_shows_error(self, checkout_info_ready: CheckoutInfoPage):
        checkout_info_ready.fill_info("João", "Silva", "")
        checkout_info_ready.click_continue()

        assert checkout_info_ready.is_error_visible()
        assert "Postal Code is required" in checkout_info_ready.get_error_message()

    def test_all_fields_empty_shows_error(self, checkout_info_ready: CheckoutInfoPage):
        checkout_info_ready.fill_info("", "", "")
        checkout_info_ready.click_continue()

        assert checkout_info_ready.is_error_visible()

    def test_valid_form_navigates_to_overview(self, checkout_info_ready: CheckoutInfoPage):
        checkout_info_ready.submit("João", "Silva", "01310-100")

        WebAssertions.assert_url_contains(checkout_info_ready._driver, "checkout-step-two")

    def test_cancel_returns_to_cart(self, checkout_info_ready: CheckoutInfoPage):
        checkout_info_ready.click_cancel()

        WebAssertions.assert_url_contains(checkout_info_ready._driver, "cart")

    def test_checkout_info_page_title(self, checkout_info_ready: CheckoutInfoPage):
        assert checkout_info_ready.get_page_title() == "Checkout: Your Information"


# ──────────────────────────────────────────────────────────────────────────────
# Checkout Overview
# ──────────────────────────────────────────────────────────────────────────────

class TestCheckoutOverview:
    """Order summary page — prices, totals, navigation."""

    def test_overview_page_title(self, checkout_overview_ready: CheckoutOverviewPage):
        assert checkout_overview_ready.get_page_title() == "Checkout: Overview"

    def test_overview_shows_purchased_item(self, checkout_overview_ready: CheckoutOverviewPage):
        assert len(checkout_overview_ready.get_item_names()) >= 1

    def test_total_equals_subtotal_plus_tax(self, checkout_overview_ready: CheckoutOverviewPage):
        subtotal = checkout_overview_ready.get_subtotal_value()
        tax      = checkout_overview_ready.get_tax_value()
        total    = checkout_overview_ready.get_total_value()

        assert round(subtotal + tax, 2) == total

    def test_subtotal_is_positive(self, checkout_overview_ready: CheckoutOverviewPage):
        assert checkout_overview_ready.get_subtotal_value() > 0

    def test_tax_is_positive(self, checkout_overview_ready: CheckoutOverviewPage):
        assert checkout_overview_ready.get_tax_value() > 0

    def test_cancel_from_overview_returns_to_inventory(
        self, checkout_overview_ready: CheckoutOverviewPage
    ):
        checkout_overview_ready.click_cancel()
        WebAssertions.assert_url_contains(checkout_overview_ready._driver, "inventory")


# ──────────────────────────────────────────────────────────────────────────────
# Checkout Complete
# ──────────────────────────────────────────────────────────────────────────────

class TestCheckoutComplete:
    """Order confirmation page."""

    def test_confirmation_header_contains_thank_you(
        self, checkout_overview_ready: CheckoutOverviewPage
    ):
        checkout_overview_ready.click_finish()
        assert CheckoutCompletePage(checkout_overview_ready._driver).is_order_confirmed()

    def test_confirmation_url(self, checkout_overview_ready: CheckoutOverviewPage):
        checkout_overview_ready.click_finish()
        WebAssertions.assert_url_contains(checkout_overview_ready._driver, "checkout-complete")

    def test_confirmation_image_is_visible(self, checkout_overview_ready: CheckoutOverviewPage):
        checkout_overview_ready.click_finish()
        assert CheckoutCompletePage(checkout_overview_ready._driver).is_confirmation_image_visible()

    def test_back_home_returns_to_inventory(self, checkout_overview_ready: CheckoutOverviewPage):
        checkout_overview_ready.click_finish()
        complete = CheckoutCompletePage(checkout_overview_ready._driver)
        complete.click_back_home()
        WebAssertions.assert_url_contains(complete._driver, "inventory")

    def test_confirmation_page_title(self, checkout_overview_ready: CheckoutOverviewPage):
        checkout_overview_ready.click_finish()
        assert CheckoutCompletePage(checkout_overview_ready._driver).get_page_title() == "Checkout: Complete!"