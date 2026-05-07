from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """
    Page Object for /cart.html (shopping cart).
    Handles item inspection, removal and checkout navigation.
    """

    PATH = "/cart.html"

    # ── Locators ───────────────────────────────────────────────────────────
    _PAGE_TITLE        = (By.CLASS_NAME, "title")
    _CART_ITEMS        = (By.CLASS_NAME, "cart_item")
    _ITEM_NAME         = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICE        = (By.CLASS_NAME, "inventory_item_price")
    _ITEM_QUANTITY     = (By.CLASS_NAME, "cart_quantity")
    _REMOVE_BUTTON     = (By.CSS_SELECTOR, ".cart_item button")
    _CHECKOUT_BUTTON   = (By.ID, "checkout")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    # ── Navigation ─────────────────────────────────────────────────────────

    def open(self) -> "CartPage":
        super().open(self.PATH)
        return self

    # ── Actions ────────────────────────────────────────────────────────────

    def remove_item_by_name(self, product_name: str) -> "CartPage":
        items = self._find_all(*self._CART_ITEMS)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip() == product_name:
                item.find_element(By.TAG_NAME, "button").click()
                return self
        raise ValueError(f"Product '{product_name}' not found in cart.")

    def remove_first_item(self) -> "CartPage":
        self._click(*self._REMOVE_BUTTON)
        return self

    def go_to_checkout(self) -> None:
        self._click(*self._CHECKOUT_BUTTON)
        self._wait_for_url(
            "checkout-step-one",
            "Checkout info page did not load after clicking checkout button"
        )

    def continue_shopping(self) -> None:
        self._click(*self._CONTINUE_SHOPPING)
        self._wait_for_url(
            "inventory",
            "Inventory page did not load after clicking continue shopping"
        )

    # ── Queries ────────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self._get_text(*self._PAGE_TITLE)

    def get_item_count(self) -> int:
        return len(self._find_all(*self._CART_ITEMS))

    def get_item_names(self) -> list[str]:
        return [el.text.strip() for el in self._find_all(*self._ITEM_NAME)]

    def get_item_prices(self) -> list[str]:
        return [el.text.strip() for el in self._find_all(*self._ITEM_PRICE)]

    def get_item_quantities(self) -> list[int]:
        return [int(el.text.strip()) for el in self._find_all(*self._ITEM_QUANTITY)]

    def is_empty(self) -> bool:
        return self.get_item_count() == 0