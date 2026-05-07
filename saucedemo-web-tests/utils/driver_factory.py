from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config.settings import settings


class DriverFactory:
    """
    Factory pattern: centralizes WebDriver creation and teardown.
    Keeps test files completely free of browser-setup boilerplate.
    """

    @staticmethod
    def create_driver() -> webdriver.Chrome:
        options = ChromeOptions()

        # ── Headless ───────────────────────────────────────────────────────
        if settings.HEADLESS:
            options.add_argument("--headless=new")

        # ── Estabilidade no CI ─────────────────────────────────────────────
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        # ── Bloquear popups que interferem nos cliques ─────────────────────
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-features=PasswordManagerEnabled")
        options.add_argument("--disable-features=TranslateUI")

        # ── Desabilitar automação banners ──────────────────────────────────
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # ── Desabilitar popups via prefs ───────────────────────────────────
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.automatic_downloads": 1,
        }
        options.add_experimental_option("prefs", prefs)

        # ── Selenium Manager cuida do driver automaticamente ───────────────
        driver = webdriver.Chrome(options=options)

        # ── IMPORTANTE: implicit_wait ZERADO ──────────────────────────────
        # Usar implicit_wait junto com WebDriverWait causa comportamento
        # imprevisível. Todo o controle de espera é feito via WebDriverWait
        # explícito no BasePage.
        driver.implicitly_wait(0)
        driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)

        return driver