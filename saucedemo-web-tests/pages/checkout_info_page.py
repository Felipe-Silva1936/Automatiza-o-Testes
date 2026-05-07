from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    """
    Page Object for /checkout-step-one.html (buyer information form).
    """

    PATH = "/checkout-step-one.html"

    # ── Locators ───────────────────────────────────────────────────────────
    _PAGE_TITLE     = (By.CLASS_NAME, "title")
    _FIRST_NAME     = (By.ID, "first-name")
    _LAST_NAME      = (By.ID, "last-name")
    _POSTAL_CODE    = (By.ID, "postal-code")
    _CONTINUE_BTN   = (By.ID, "continue")
    _CANCEL_BTN     = (By.ID, "cancel")
    _ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")

    # ── Actions ────────────────────────────────────────────────────────────

    def fill_info(self, first: str, last: str, postal: str) -> "CheckoutInfoPage":
        """Fill all checkout fields using React-compatible JS setter."""
        self._type_react(*self._FIRST_NAME, first)
        self._type_react(*self._LAST_NAME, last)
        self._type_react(*self._POSTAL_CODE, postal)
        return self

    def click_continue(self) -> None:
        btn = self._find(*self._CONTINUE_BTN)
        self._driver.execute_script("arguments[0].click();", btn)

    def click_cancel(self) -> None:
        self._click(*self._CANCEL_BTN)

    def submit(self, first: str, last: str, postal: str) -> None:
        """Fluent: fill form and continue."""
        self.fill_info(first, last, postal)
        self.click_continue()
        self._wait_for_url("checkout-step-two", "Checkout overview did not load after submitting info")

    # ── Queries ────────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self._get_text(*self._PAGE_TITLE)

    def get_error_message(self) -> str:
        return self._get_text(*self._ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self._is_visible(*self._ERROR_MESSAGE)
