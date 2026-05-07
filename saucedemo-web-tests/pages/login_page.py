from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for https://www.saucedemo.com (login screen).
    Encapsulates all login-related selectors and interactions.
    """

    PATH = "/"

    # ── Locators ───────────────────────────────────────────────────────────
    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON   = (By.ID, "login-button")
    _ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")
    _ERROR_BUTTON   = (By.CSS_SELECTOR, ".error-button")

    # ── Navigation ─────────────────────────────────────────────────────────

    def open(self) -> "LoginPage":
        super().open(self.PATH)
        # Aguarda o botão de login estar visível antes de retornar
        self._find_visible(*self._LOGIN_BUTTON)
        return self

    # ── Actions ────────────────────────────────────────────────────────────

    def enter_username(self, username: str) -> "LoginPage":
        self._type(*self._USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self._type(*self._PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        btn = self._find(*self._LOGIN_BUTTON)
        self._driver.execute_script("arguments[0].click();", btn)

    def login(self, username: str, password: str) -> None:
        """Full login flow: fill credentials and submit."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def dismiss_error(self) -> "LoginPage":
        self._click(*self._ERROR_BUTTON)
        return self

    # ── Queries ────────────────────────────────────────────────────────────

    def get_error_message(self) -> str:
        return self._get_text(*self._ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self._is_visible(*self._ERROR_MESSAGE)

    def is_login_button_visible(self) -> bool:
        return self._is_visible(*self._LOGIN_BUTTON)