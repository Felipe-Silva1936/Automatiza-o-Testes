"""
Test Suite: E2E Purchase Flow
Cobre o fluxo completo de compra do SauceDemo:
  Login → Adiciona produto → Carrinho → Checkout → Confirmação
"""
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


class TestFullPurchaseFlow:
    """Fluxo completo de compra — do login à confirmação."""

    def test_complete_purchase_flow(self, driver):
        """
        E2E: standard_user realiza uma compra completa.

        Steps:
          1. Abre o SauceDemo e faz login
          2. Adiciona 'Sauce Labs Backpack' ao carrinho
          3. Navega para o carrinho e verifica o item
          4. Inicia o checkout e preenche os dados de entrega
          5. Verifica o resumo do pedido e o cálculo do total
          6. Finaliza a compra e verifica a confirmação
        """
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

        # Step 5 — Overview: verifica item e cálculo do total
        overview = CheckoutOverviewPage(driver)
        WebAssertions.assert_url_contains(driver, "checkout-step-two")
        assert SAUCE_LABS_BACKPACK in overview.get_item_names()
        subtotal = overview.get_subtotal_value()
        tax      = overview.get_tax_value()
        total    = overview.get_total_value()
        assert round(subtotal + tax, 2) == total, (
            f"Total ({total}) ≠ subtotal ({subtotal}) + tax ({tax})"
        )

        # Step 6 — Finaliza e confirma
        overview.click_finish()
        complete = CheckoutCompletePage(driver)
        WebAssertions.assert_url_contains(driver, "checkout-complete")
        assert complete.is_order_confirmed(), "Confirmação de pedido não encontrada"