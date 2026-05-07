from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.settings import settings


class BasePage:
    """
    Abstract base Page Object.
    Usa exclusivamente WebDriverWait explícito — implicit_wait está zerado
    no driver para evitar conflitos e comportamento imprevisível.
    """

    def __init__(self, driver: WebDriver):
        self._driver = driver
        # Wait padrão baseado na config
        self._wait = WebDriverWait(driver, settings.IMPLICIT_WAIT)
        # Wait longo para ações críticas de navegação
        self._long_wait = WebDriverWait(driver, settings.IMPLICIT_WAIT * 2)

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
        self._long_wait.until(
            EC.url_contains(fragment),
            message=message or f"URL did not contain '{fragment}'"
        )

    def _wait_for_element_text(
        self, element: WebElement, expected_text: str, timeout: int = None
    ) -> None:
        """Aguarda um elemento específico ter o texto esperado."""
        wait = WebDriverWait(self._driver, timeout or settings.IMPLICIT_WAIT)
        wait.until(
            lambda d: element.text.strip().lower() == expected_text.lower(),
            message=f"Element text did not become '{expected_text}'"
        )