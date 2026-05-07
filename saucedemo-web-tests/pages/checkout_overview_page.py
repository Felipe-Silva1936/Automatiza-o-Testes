from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    """
    Page Object for /checkout-step-two.html (order summary & finish).
    """

    PATH = "/checkout-step-two.html"

    # ── Locators ───────────────────────────────────────────────────────────
    _PAGE_TITLE     = (By.CLASS_NAME, "title")
    _CART_ITEMS     = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES     = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES    = (By.CLASS_NAME, "inventory_item_price")
    _SUBTOTAL       = (By.CLASS_NAME, "summary_subtotal_label")
    _TAX            = (By.CLASS_NAME, "summary_tax_label")
    _TOTAL          = (By.CLASS_NAME, "summary_total_label")
    _FINISH_BTN     = (By.ID, "finish")
    _CANCEL_BTN     = (By.ID, "cancel")
    _PAYMENT_INFO   = (By.CLASS_NAME, "summary_value_label")

    # ── Actions ────────────────────────────────────────────────────────────

    def click_finish(self) -> None:
        self._click(*self._FINISH_BTN)

    def click_cancel(self) -> None:
        self._click(*self._CANCEL_BTN)

    # ── Queries ────────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self._get_text(*self._PAGE_TITLE)

    def get_item_count(self) -> int:
        return len(self._find_all(*self._CART_ITEMS))

    def get_item_names(self) -> list[str]:
        return [el.text.strip() for el in self._find_all(*self._ITEM_NAMES)]

    def get_subtotal_text(self) -> str:
        return self._get_text(*self._SUBTOTAL)

    def get_tax_text(self) -> str:
        return self._get_text(*self._TAX)

    def get_total_text(self) -> str:
        return self._get_text(*self._TOTAL)

    def get_subtotal_value(self) -> float:
        """Extract numeric value from 'Item total: $X.XX'."""
        text = self.get_subtotal_text()
        return float(text.split("$")[-1])

    def get_tax_value(self) -> float:
        text = self.get_tax_text()
        return float(text.split("$")[-1])

    def get_total_value(self) -> float:
        text = self.get_total_text()
        return float(text.split("$")[-1])
