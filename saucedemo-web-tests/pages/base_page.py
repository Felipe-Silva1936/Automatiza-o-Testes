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
        """
        Aguarda pelo menos um elemento antes de retornar a lista.
        Evita lista vazia em páginas SPA que carregam dinamicamente.
        """
        try:
            self._wait.until(EC.presence_of_element_located((by, locator)))
        except Exception:
            pass
        return self._driver.find_elements(by, locator)

    # ── Interactions ───────────────────────────────────────────────────────

    def _click(self, by: str, locator: str) -> None:
        self._find_clickable(by, locator).click()

    def _type(self, by: str, locator: str, text: str) -> None:
        field = self._find_visible(by, locator)
        field.clear()
        field.send_keys(text)

    _JS_SET_REACT_VALUE = """
        var setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
        ).set;
        setter.call(arguments[0], arguments[1]);
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """

    def _type_react(self, by: str, locator: str, text: str) -> None:
        """Sets value on React-controlled inputs via the native setter + synthetic events."""
        field = self._find(by, locator)
        self._driver.execute_script(self._JS_SET_REACT_VALUE, field, text)

    def _get_text(self, by: str, locator: str) -> str:
        return self._find_visible(by, locator).text.strip()

    def _is_visible(self, by: str, locator: str, timeout: int = 3) -> bool:
        """
        Usa timeout curto para verificações booleanas.
        Evita esperar o timeout cheio em assertions negativas.
        """
        try:
            WebDriverWait(self._driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except Exception:
            return False

    def _wait_for_url(self, fragment: str, message: str = "") -> None:
        """Aguarda a URL conter o fragmento especificado."""
        self._wait.until(
            EC.url_contains(fragment),
            message=message or f"URL did not contain '{fragment}'"
        )