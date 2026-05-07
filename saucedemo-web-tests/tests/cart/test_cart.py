"""
Test Suite: Shopping Cart
Covers: add items, badge count, cart content, remove items, quantities.
"""
import pytest
from pages import InventoryPage, CartPage
from utils.assertions import WebAssertions
from config.settings import settings


SAUCE_LABS_BACKPACK    = "Sauce Labs Backpack"
SAUCE_LABS_BIKE_LIGHT  = "Sauce Labs Bike Light"
SAUCE_LABS_BOLT_SHIRT  = "Sauce Labs Bolt T-Shirt"


class TestAddToCart:
    """Adding items to the cart."""

    def test_add_one_item_updates_badge(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)

        assert authenticated_inventory.get_cart_item_count() == 1

    def test_add_two_items_updates_badge(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BIKE_LIGHT)

        assert authenticated_inventory.get_cart_item_count() == 2

    def test_add_three_items_updates_badge(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BIKE_LIGHT)
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BOLT_SHIRT)

        assert authenticated_inventory.get_cart_item_count() == 3

    def test_cart_badge_not_visible_before_adding(self, authenticated_inventory: InventoryPage):
        assert authenticated_inventory.get_cart_item_count() == 0


class TestCartContent:
    """Cart page shows correct items and details."""

    def test_cart_shows_added_item_name(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.go_to_cart()

        cart = CartPage(authenticated_inventory._driver)
        assert SAUCE_LABS_BACKPACK in cart.get_item_names()

    def test_cart_item_has_correct_quantity(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.go_to_cart()

        cart = CartPage(authenticated_inventory._driver)
        quantities = cart.get_item_quantities()
        assert all(q == 1 for q in quantities), "Each item should have quantity 1"

    def test_cart_shows_two_added_items(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BIKE_LIGHT)
        authenticated_inventory.go_to_cart()

        cart = CartPage(authenticated_inventory._driver)
        WebAssertions.assert_items_count(cart.get_item_count(), 2, "cart items")

    def test_cart_item_price_format(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.go_to_cart()

        cart = CartPage(authenticated_inventory._driver)
        for price in cart.get_item_prices():
            WebAssertions.assert_price_format(price)

    def test_cart_page_title(self, cart_with_one_item: CartPage):
        assert cart_with_one_item.get_page_title() == "Your Cart"

    def test_cart_url(self, cart_with_one_item: CartPage):
        WebAssertions.assert_url_contains(cart_with_one_item._driver, "cart")


class TestRemoveFromCart:
    """Removing items from the cart."""

    def test_remove_item_empties_cart(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.go_to_cart()

        cart = CartPage(authenticated_inventory._driver)
        cart.remove_item_by_name(SAUCE_LABS_BACKPACK)

        assert cart.is_empty(), "Cart should be empty after removing the only item"

    def test_remove_one_of_two_items_leaves_one(self, authenticated_inventory: InventoryPage):
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BACKPACK)
        authenticated_inventory.add_item_to_cart_by_name(SAUCE_LABS_BIKE_LIGHT)
        authenticated_inventory.go_to_cart()

        cart = CartPage(authenticated_inventory._driver)
        cart.remove_item_by_name(SAUCE_LABS_BACKPACK)

        WebAssertions.assert_items_count(cart.get_item_count(), 1, "cart items")
        assert SAUCE_LABS_BIKE_LIGHT in cart.get_item_names()

    def test_continue_shopping_returns_to_inventory(self, cart_with_one_item: CartPage):
        cart_with_one_item.continue_shopping()

        WebAssertions.assert_url_contains(cart_with_one_item._driver, "inventory")
