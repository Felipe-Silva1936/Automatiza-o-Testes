import requests
from clients.base_client import BaseClient


class StoreClient(BaseClient):
    """
    Service Object for the /store endpoint group.
    Encapsulates all store-related API interactions.
    """

    ENDPOINT = "/store"

    def get_inventory(self) -> requests.Response:
        """GET /store/inventory — Returns pet inventories by status."""
        return self.get(f"{self.ENDPOINT}/inventory")

    def place_order(self, payload: dict) -> requests.Response:
        """POST /store/order — Place an order for a pet."""
        return self.post(f"{self.ENDPOINT}/order", payload)

    def get_order_by_id(self, order_id: int) -> requests.Response:
        """GET /store/order/{orderId} — Find purchase order by ID."""
        return self.get(f"{self.ENDPOINT}/order/{order_id}")

    def delete_order(self, order_id: int) -> requests.Response:
        """DELETE /store/order/{orderId} — Delete purchase order by ID."""
        return self.delete(f"{self.ENDPOINT}/order/{order_id}")
