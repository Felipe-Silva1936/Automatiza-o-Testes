from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class WebAssertions:
    """
    Helper Object with focused, reusable web assertions.
    Each method has an explicit failure message for fast debugging.
    """

    @staticmethod
    def assert_url_contains(driver: WebDriver, fragment: str) -> None:
        current = driver.current_url
        assert fragment in current, (
            f"Expected URL to contain '{fragment}', got: '{current}'"
        )

    @staticmethod
    def assert_url_equals(driver: WebDriver, expected: str) -> None:
        current = driver.current_url
        assert current == expected, (
            f"Expected URL '{expected}', got: '{current}'"
        )

    @staticmethod
    def assert_title_contains(driver: WebDriver, text: str) -> None:
        title = driver.title
        assert text in title, (
            f"Expected page title to contain '{text}', got: '{title}'"
        )

    @staticmethod
    def assert_element_visible(element: WebElement, label: str = "element") -> None:
        assert element.is_displayed(), f"Expected '{label}' to be visible, but it was not."

    @staticmethod
    def assert_element_text(element: WebElement, expected: str, label: str = "element") -> None:
        actual = element.text.strip()
        assert actual == expected, (
            f"'{label}' text: expected '{expected}', got '{actual}'"
        )

    @staticmethod
    def assert_element_text_contains(element: WebElement, fragment: str, label: str = "element") -> None:
        actual = element.text.strip()
        assert fragment in actual, (
            f"'{label}' text should contain '{fragment}', got '{actual}'"
        )

    @staticmethod
    def assert_items_count(actual: int, expected: int, label: str = "items") -> None:
        assert actual == expected, (
            f"Expected {expected} {label}, got {actual}"
        )

    @staticmethod
    def assert_price_format(price_text: str) -> None:
        import re
        assert re.match(r"^\$\d+\.\d{2}$", price_text), (
            f"Price '{price_text}' does not match expected format '$X.XX'"
        )
