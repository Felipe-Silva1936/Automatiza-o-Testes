from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """
    Page Object for /checkout-complete.html (order confirmation).
    """

    PATH = "/checkout-complete.html"

    # ── Locators ───────────────────────────────────────────────────────────
    _PAGE_TITLE      = (By.CLASS_NAME, "title")
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    _COMPLETE_TEXT   = (By.CLASS_NAME, "complete-text")
    _PONY_EXPRESS    = (By.CLASS_NAME, "pony_express")
    _BACK_HOME_BTN   = (By.ID, "back-to-products")

    # ── Actions ────────────────────────────────────────────────────────────

    def click_back_home(self) -> None:
        self._click(*self._BACK_HOME_BTN)
        self._wait_for_url(
            "inventory",
            "Inventory page did not load after clicking back home"
        )

    # ── Queries ────────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self._get_text(*self._PAGE_TITLE)

    def get_confirmation_header(self) -> str:
        return self._get_text(*self._COMPLETE_HEADER)

    def get_confirmation_text(self) -> str:
        return self._get_text(*self._COMPLETE_TEXT)

    def is_confirmation_image_visible(self) -> bool:
        return self._is_visible(*self._PONY_EXPRESS)

    def is_order_confirmed(self) -> bool:
        """Convenience: returns True when the thank-you header is shown."""
        return "Thank you" in self.get_confirmation_header()