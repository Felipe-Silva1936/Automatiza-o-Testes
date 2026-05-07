"""
Test Suite: Store Endpoints
Covers: GET /store/inventory, POST /store/order,
        GET /store/order/{id}, DELETE /store/order/{id}
"""
import pytest
from clients import StoreClient
from models import OrderBuilder
from utils import ResponseAssertions, DataGenerator


class TestStoreInventory:
    """Tests for GET /store/inventory"""

    def test_get_inventory_returns_200(self, store_client: StoreClient):
        response = store_client.get_inventory()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_content_type_json(response)
        ResponseAssertions.assert_response_time(response)

    def test_get_inventory_returns_dict(self, store_client: StoreClient):
        response = store_client.get_inventory()
        body = response.json()

        ResponseAssertions.assert_ok(response)
        assert isinstance(body, dict), f"Expected dict, got {type(body)}"
        assert len(body) > 0, "Inventory should not be empty"

    def test_get_inventory_has_numeric_values(self, store_client: StoreClient):
        response = store_client.get_inventory()
        body = response.json()

        ResponseAssertions.assert_ok(response)
        for key, value in body.items():
            assert isinstance(value, int), (
                f"Inventory value for '{key}' should be int, got {type(value)}"
            )


class TestStoreOrderCreate:
    """Tests for POST /store/order"""

    def test_place_order_returns_200(self, store_client: StoreClient, new_order_payload: dict):
        response = store_client.place_order(new_order_payload)

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_content_type_json(response)

    def test_place_order_contains_required_fields(self, store_client: StoreClient, new_order_payload: dict):
        response = store_client.place_order(new_order_payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_present(body, "id", "petId", "quantity", "status")

    def test_place_order_status_is_placed(self, store_client: StoreClient, new_order_payload: dict):
        response = store_client.place_order(new_order_payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "status", "placed")

    def test_place_order_quantity_matches(self, store_client: StoreClient, new_order_payload: dict):
        response = store_client.place_order(new_order_payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "quantity", new_order_payload["quantity"])

    def test_place_order_with_approved_status(self, store_client: StoreClient):
        payload = (
            OrderBuilder()
            .with_id(DataGenerator.unique_id() % 10 + 1)
            .with_pet_id(DataGenerator.unique_id())
            .with_quantity(5)
            .with_status("approved")
            .build()
            .to_dict()
        )

        response = store_client.place_order(payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "status", "approved")


class TestStoreOrderRead:
    """Tests for GET /store/order/{orderId}"""

    def test_get_order_by_id_returns_200(self, store_client: StoreClient, created_order: dict):
        response = store_client.get_order_by_id(created_order["id"])

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_content_type_json(response)

    def test_get_order_returns_correct_id(self, store_client: StoreClient, created_order: dict):
        order_id = created_order["id"]
        response = store_client.get_order_by_id(order_id)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "id", order_id)

    def test_get_order_returns_correct_quantity(self, store_client: StoreClient, created_order: dict):
        response = store_client.get_order_by_id(created_order["id"])
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "quantity", created_order["quantity"])

    def test_get_nonexistent_order_returns_404(self, store_client: StoreClient):
        response = store_client.get_order_by_id(999999)

        ResponseAssertions.assert_not_found(response)


class TestStoreOrderDelete:
    """Tests for DELETE /store/order/{orderId}"""

    def test_delete_order_returns_200(self, store_client: StoreClient, new_order_payload: dict):
        create_resp = store_client.place_order(new_order_payload)
        assert create_resp.status_code == 200
        order_id = create_resp.json()["id"]

        delete_resp = store_client.delete_order(order_id)
        ResponseAssertions.assert_ok(delete_resp)

    def test_deleted_order_is_no_longer_found(self, store_client: StoreClient, new_order_payload: dict):
        create_resp = store_client.place_order(new_order_payload)
        assert create_resp.status_code == 200
        order_id = create_resp.json()["id"]

        store_client.delete_order(order_id)
        get_resp = store_client.get_order_by_id(order_id)

        ResponseAssertions.assert_not_found(get_resp)
