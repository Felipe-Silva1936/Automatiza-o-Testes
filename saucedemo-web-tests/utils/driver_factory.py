from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from config.settings import settings


class DriverFactory:
    """
    Factory pattern: centralizes WebDriver creation and teardown.
    Keeps test files completely free of browser-setup boilerplate.
    """

    @staticmethod
    def create_driver() -> webdriver.Chrome:
        options = ChromeOptions()

        if settings.HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        # Disable automation banners
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.chrome(options=options )
        driver.implicitly_wait(settings.IMPLICIT_WAIT)
        driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)
        return driver
