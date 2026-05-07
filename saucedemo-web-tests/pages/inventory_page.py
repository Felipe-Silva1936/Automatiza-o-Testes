from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """
    Page Object for /inventory.html (product listing).
    Handles product discovery, sorting and cart badge.
    """

    PATH = "/inventory.html"

    # ── Locators ───────────────────────────────────────────────────────────
    _PAGE_TITLE      = (By.CLASS_NAME, "title")
    _INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAME       = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICE      = (By.CLASS_NAME, "inventory_item_price")
    _SORT_DROPDOWN   = (By.CLASS_NAME, "product_sort_container")
    _CART_BADGE      = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK       = (By.CLASS_NAME, "shopping_cart_link")
    _BURGER_MENU     = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK     = (By.ID, "logout_sidebar_link")
    _ADD_TO_CART_BTN = (By.CSS_SELECTOR, ".inventory_item button")

    # ── Navigation ─────────────────────────────────────────────────────────

    def open(self) -> "InventoryPage":
        super().open(self.PATH)
        return self

    def wait_until_ready(self) -> "InventoryPage":
        """
        Aguarda a página estar completamente carregada.
        Garante que os botões Add to cart estão interativos.
        """
        self._wait.until(
            EC.element_to_be_clickable(self._ADD_TO_CART_BTN),
            message="Inventory page not ready: Add to cart button not clickable"
        )
        return self

    # ── Actions ────────────────────────────────────────────────────────────

    def add_item_to_cart_by_name(self, product_name: str) -> "InventoryPage":
        """Click 'Add to cart' for a product matched by exact name."""
        self.wait_until_ready()
        items = self._find_all(*self._INVENTORY_ITEMS)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip() == product_name:
                btn = item.find_element(By.TAG_NAME, "button")
                self._wait.until(
                    EC.element_to_be_clickable(btn),
                    message=f"Add to cart button for '{product_name}' not clickable"
                )
                btn.click()
                # Aguarda o botão mudar para "Remove" — confirma que o item foi adicionado
                self._wait.until(
                    lambda d: item.find_element(By.TAG_NAME, "button").text.strip().lower() == "remove",
                    message=f"Button did not change to 'Remove' after adding '{product_name}'"
                )
                return self
        raise ValueError(f"Product '{product_name}' not found in inventory.")

    def add_first_item_to_cart(self) -> "InventoryPage":
        self.wait_until_ready()
        items = self._find_all(*self._INVENTORY_ITEMS)
        item = items[0]
        btn = item.find_element(By.TAG_NAME, "button")
        self._wait.until(
            EC.element_to_be_clickable(btn),
            message="Add to cart button for first item not clickable"
        )
        btn.click()
        # Aguarda o botão mudar para "Remove" — confirma que o item foi adicionado
        self._wait.until(
            lambda d: item.find_element(By.TAG_NAME, "button").text.strip().lower() == "remove",
            message="Button did not change to 'Remove' after adding first item"
        )
        return self

    def get_first_item_name(self) -> str:
        items = self._find_all(*self._INVENTORY_ITEMS)
        return items[0].find_element(By.CLASS_NAME, "inventory_item_name").text.strip()

    def get_first_item_price(self) -> str:
        items = self._find_all(*self._INVENTORY_ITEMS)
        return items[0].find_element(By.CLASS_NAME, "inventory_item_price").text.strip()

    def go_to_cart(self) -> None:
        self._click(*self._CART_LINK)
        self._wait_for_url("cart", "Cart page did not load after clicking cart link")

    def logout(self) -> None:
        self._click(*self._BURGER_MENU)
        self._click(*self._LOGOUT_LINK)
        self._wait.until(
            lambda d: "inventory" not in d.current_url and "cart" not in d.current_url,
            message="Login page did not load after logout"
        )

    def select_sort(self, value: str) -> "InventoryPage":
        """Sort products. Values: 'az', 'za', 'lohi', 'hilo'."""
        from selenium.webdriver.support.ui import Select
        dropdown = self._find(*self._SORT_DROPDOWN)
        Select(dropdown).select_by_value(value)
        return self

    # ── Queries ────────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self._get_text(*self._PAGE_TITLE)

    def get_cart_item_count(self) -> int:
        badge = self._find_all(*self._CART_BADGE)
        return int(badge[0].text) if badge else 0

    def get_all_item_names(self) -> list[str]:
        return [el.text.strip() for el in self._find_all(*self._ITEM_NAME)]

    def get_all_item_prices(self) -> list[float]:
        prices = self._find_all(*self._ITEM_PRICE)
        return [float(p.text.replace("$", "")) for p in prices]

    def get_item_count(self) -> int:
        return len(self._find_all(*self._INVENTORY_ITEMS))