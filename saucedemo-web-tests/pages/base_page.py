from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.settings import settings


class BasePage:
    """
    Abstract base Page Object.
    Provides shared WebDriver helpers so subclasses stay free of boilerplate.
    All element interactions go through these protected methods for consistency.
    """

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(driver, settings.IMPLICIT_WAIT)

    # ── Navigation ─────────────────────────────────────────────────────────

    def open(self, path: str = "") -> None:
        self._driver.get(f"{settings.BASE_URL}{path}")

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    @property
    def page_title(self) -> str:
        return self._driver.title

    # ── Element finders ────────────────────────────────────────────────────

    def _find(self, by: str, locator: str) -> WebElement:
        return self._wait.until(
            EC.presence_of_element_located((by, locator)),
            message=f"Element not found: [{by}] '{locator}'"
        )

    def _find_visible(self, by: str, locator: str) -> WebElement:
        return self._wait.until(
            EC.visibility_of_element_located((by, locator)),
            message=f"Element not visible: [{by}] '{locator}'"
        )

    def _find_clickable(self, by: str, locator: str) -> WebElement:
        return self._wait.until(
            EC.element_to_be_clickable((by, locator)),
            message=f"Element not clickable: [{by}] '{locator}'"
        )

    def _find_all(self, by: str, locator: str) -> list[WebElement]:
        return self._driver.find_elements(by, locator)

    # ── Interactions ───────────────────────────────────────────────────────

    def _click(self, by: str, locator: str) -> None:
        self._find_clickable(by, locator).click()

    def _type(self, by: str, locator: str, text: str) -> None:
        field = self._find_visible(by, locator)
        field.clear()
        field.send_keys(text)

    def _get_text(self, by: str, locator: str) -> str:
        return self._find_visible(by, locator).text.strip()

    def _is_visible(self, by: str, locator: str) -> bool:
        try:
            return self._find_visible(by, locator).is_displayed()
        except Exception:
            return False
