import requests
from clients.base_client import BaseClient


class PetClient(BaseClient):
    """
    Service Object for the /pet endpoint group.
    Encapsulates all pet-related API interactions.
    """

    ENDPOINT = "/pet"

    def add_pet(self, payload: dict) -> requests.Response:
        """POST /pet — Add a new pet to the store."""
        return self.post(self.ENDPOINT, payload)

    def update_pet(self, payload: dict) -> requests.Response:
        """PUT /pet — Update an existing pet."""
        return self.put(self.ENDPOINT, payload)

    def get_pets_by_status(self, status: str) -> requests.Response:
        """GET /pet/findByStatus — Finds pets by status."""
        return self.get(f"{self.ENDPOINT}/findByStatus", params={"status": status})

    def get_pet_by_id(self, pet_id: int) -> requests.Response:
        """GET /pet/{petId} — Find pet by ID."""
        return self.get(f"{self.ENDPOINT}/{pet_id}")

    def update_pet_with_form(self, pet_id: int, name: str = None, status: str = None) -> requests.Response:
        """POST /pet/{petId} — Updates a pet in the store with form data."""
        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        return self.post_form(f"{self.ENDPOINT}/{pet_id}", data=data)

    def delete_pet(self, pet_id: int) -> requests.Response:
        """DELETE /pet/{petId} — Deletes a pet."""
        return self.delete(f"{self.ENDPOINT}/{pet_id}")
