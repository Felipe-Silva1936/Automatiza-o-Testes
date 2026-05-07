"""
Test Suite: Authentication
Covers: login success, login failure, locked user, field validation, logout.
"""
import pytest
from pages import LoginPage, InventoryPage
from utils.assertions import WebAssertions
from config.settings import settings


class TestLoginSuccess:
    """Valid credential scenarios."""

    def test_login_redirects_to_inventory(self, login_page: LoginPage):
        login_page.open()
        login_page.login(settings.STANDARD_USER, settings.PASSWORD)

        WebAssertions.assert_url_contains(login_page._driver, "inventory")

    def test_inventory_page_title_after_login(self, login_page: LoginPage):
        login_page.open()
        login_page.login(settings.STANDARD_USER, settings.PASSWORD)

        inventory = InventoryPage(login_page._driver)
        assert inventory.get_page_title() == "Products"

    def test_inventory_shows_items_after_login(self, login_page: LoginPage):
        login_page.open()
        login_page.login(settings.STANDARD_USER, settings.PASSWORD)

        inventory = InventoryPage(login_page._driver)
        assert inventory.get_item_count() == 6, "Inventory should show 6 products"

    def test_login_button_is_present_on_load(self, login_page: LoginPage):
        login_page.open()
        assert login_page.is_login_button_visible()


class TestLoginFailure:
    """Invalid credential and validation scenarios."""

    def test_wrong_password_shows_error(self, login_page: LoginPage):
        login_page.open()
        login_page.login(settings.STANDARD_USER, "wrong_password")

        assert login_page.is_error_visible()

    def test_wrong_password_error_message_content(self, login_page: LoginPage):
        login_page.open()
        login_page.login(settings.STANDARD_USER, "wrong_password")

        error = login_page.get_error_message()
        assert "Username and password do not match" in error

    def test_empty_username_shows_error(self, login_page: LoginPage):
        login_page.open()
        login_page.login("", settings.PASSWORD)

        assert login_page.is_error_visible()
        assert "Username is required" in login_page.get_error_message()

    def test_empty_password_shows_error(self, login_page: LoginPage):
        login_page.open()
        login_page.login(settings.STANDARD_USER, "")

        assert login_page.is_error_visible()
        assert "Password is required" in login_page.get_error_message()

    def test_locked_user_shows_error(self, login_page: LoginPage):
        login_page.open()
        login_page.login(settings.LOCKED_USER, settings.PASSWORD)

        assert login_page.is_error_visible()
        assert "locked out" in login_page.get_error_message()

    def test_error_is_dismissible(self, login_page: LoginPage):
        login_page.open()
        login_page.login("", "")
        assert login_page.is_error_visible()

        login_page.dismiss_error()
        assert not login_page.is_error_visible()

    def test_failed_login_stays_on_login_page(self, login_page: LoginPage):
        login_page.open()
        login_page.login("nonexistent_user", "badpass")

        WebAssertions.assert_url_contains(login_page._driver, "saucedemo.com")
        assert login_page.is_login_button_visible()


class TestLogout:
    """Logout flow."""

    def test_logout_redirects_to_login(self, authenticated_inventory):
        authenticated_inventory.logout()

        WebAssertions.assert_url_contains(
            authenticated_inventory._driver, "saucedemo.com"
        )
        login = LoginPage(authenticated_inventory._driver)
        assert login.is_login_button_visible()
