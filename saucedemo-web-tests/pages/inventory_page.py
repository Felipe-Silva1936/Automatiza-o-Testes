from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        """Aguarda os botões Add to cart estarem presentes no DOM."""
        self._wait.until(
            EC.presence_of_element_located(self._ADD_TO_CART_BTN),
            message="Inventory page not ready: Add to cart button not found"
        )
        return self

    # ── Actions ────────────────────────────────────────────────────────────

    def add_item_to_cart_by_name(self, product_name: str) -> "InventoryPage":
        """Click 'Add to cart' via JavaScript — bypassa overlays e popups."""
        self.wait_until_ready()
        items = self._find_all(*self._INVENTORY_ITEMS)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text.strip() == product_name:
                btn = item.find_element(By.TAG_NAME, "button")
                # JS click — não depende de visibilidade nem interatividade
                self._driver.execute_script("arguments[0].click();", btn)
                # Aguarda botão mudar para "Remove" como confirmação
                self._wait_for_element_text(btn, "remove")
                return self
        raise ValueError(f"Product '{product_name}' not found in inventory.")

    def add_first_item_to_cart(self) -> "InventoryPage":
        self.wait_until_ready()
        items = self._find_all(*self._INVENTORY_ITEMS)
        btn = items[0].find_element(By.TAG_NAME, "button")
        # JS click — não depende de visibilidade nem interatividade
        self._driver.execute_script("arguments[0].click();", btn)
        # Aguarda botão mudar para "Remove" como confirmação
        self._wait_for_element_text(btn, "remove")
        return self

    def get_first_item_name(self) -> str:
        items = self._find_all(*self._INVENTORY_ITEMS)
        return items[0].find_element(By.CLASS_NAME, "inventory_item_name").text.strip()

    def get_first_item_price(self) -> str:
        items = self._find_all(*self._INVENTORY_ITEMS)
        return items[0].find_element(By.CLASS_NAME, "inventory_item_price").text.strip()

    def go_to_cart(self) -> None:
        cart_link = self._find_clickable(*self._CART_LINK)
        # JS click — consistent with add-to-cart; avoids React re-render race condition
        self._driver.execute_script("arguments[0].click();", cart_link)
        self._wait_for_url("cart", "Cart page did not load after clicking cart link")

    def logout(self) -> None:
        self._click(*self._BURGER_MENU)
        self._click(*self._LOGOUT_LINK)
        self._long_wait.until(
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