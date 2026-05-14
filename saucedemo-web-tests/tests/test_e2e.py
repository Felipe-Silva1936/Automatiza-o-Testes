
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

class TestFullPurchaseFlow:

    def test_complete_purchase_flow(self, driver):
      
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