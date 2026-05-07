"""
Test Suite: Pet Endpoints
Covers: POST /pet, PUT /pet, GET /pet/findByStatus, GET /pet/{id},
        POST /pet/{id} (form), DELETE /pet/{id}
"""
import pytest
from clients import PetClient
from models import PetBuilder
from utils import ResponseAssertions, DataGenerator


class TestPetCreate:
    """Tests for POST /pet"""

    def test_add_pet_returns_200(self, pet_client: PetClient, new_pet_payload: dict):
        response = pet_client.add_pet(new_pet_payload)

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_content_type_json(response)
        ResponseAssertions.assert_response_time(response)

    def test_add_pet_returns_correct_name(self, pet_client: PetClient, new_pet_payload: dict):
        response = pet_client.add_pet(new_pet_payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "name", new_pet_payload["name"])

    def test_add_pet_returns_correct_status(self, pet_client: PetClient, new_pet_payload: dict):
        response = pet_client.add_pet(new_pet_payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "status", "available")

    def test_add_pet_contains_required_fields(self, pet_client: PetClient, new_pet_payload: dict):
        response = pet_client.add_pet(new_pet_payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_present(body, "id", "name", "status", "photoUrls")

    def test_add_pet_with_all_fields(self, pet_client: PetClient):
        payload = (
            PetBuilder()
            .with_id(DataGenerator.unique_id())
            .with_name("Rex")
            .with_status("pending")
            .with_category(2, "Cats")
            .with_tag(10, "vaccinated")
            .with_photo_urls(["https://example.com/rex.jpg"])
            .build()
            .to_dict()
        )

        response = pet_client.add_pet(payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        assert body["category"]["name"] == "Cats"
        assert body["tags"][0]["name"] == "vaccinated"
        assert body["status"] == "pending"


class TestPetRead:
    """Tests for GET /pet/findByStatus and GET /pet/{id}"""

    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status_returns_list(self, pet_client: PetClient, status: str):
        response = pet_client.get_pets_by_status(status)

        ResponseAssertions.assert_ok(response)
        body = response.json()
        assert isinstance(body, list), f"Expected list for status '{status}', got {type(body)}"

    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status_all_match(self, pet_client: PetClient, status: str):
        response = pet_client.get_pets_by_status(status)

        ResponseAssertions.assert_ok(response)
        pets = response.json()
        for pet in pets:
            assert pet.get("status") == status, (
                f"Pet {pet.get('id')} has status '{pet.get('status')}', expected '{status}'"
            )

    def test_get_pet_by_id_returns_correct_pet(self, pet_client: PetClient, created_pet: dict):
        pet_id = created_pet["id"]
        response = pet_client.get_pet_by_id(pet_id)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "id", pet_id)
        ResponseAssertions.assert_field_equals(body, "name", created_pet["name"])

    def test_get_pet_by_nonexistent_id_returns_404(self, pet_client: PetClient, new_pet_payload: dict):
        # Cria um pet, deleta ele e então busca pelo ID deletado
        # Garante que o ID não existe independente do estado da API pública
        create_resp = pet_client.add_pet(new_pet_payload)
        assert create_resp.status_code == 200, "Falha ao criar pet para o teste"
        pet_id = create_resp.json()["id"]

        pet_client.delete_pet(pet_id)

        response = pet_client.get_pet_by_id(pet_id)
        ResponseAssertions.assert_not_found(response)


class TestPetUpdate:
    """Tests for PUT /pet and POST /pet/{id} (form data)"""

    def test_update_pet_name_returns_200(self, pet_client: PetClient, created_pet: dict):
        updated_payload = {**created_pet, "name": "UpdatedName"}
        response = pet_client.update_pet(updated_payload)

        ResponseAssertions.assert_ok(response)
        body = response.json()
        ResponseAssertions.assert_field_equals(body, "name", "UpdatedName")

    def test_update_pet_status_returns_200(self, pet_client: PetClient, created_pet: dict):
        updated_payload = {**created_pet, "status": "sold"}
        response = pet_client.update_pet(updated_payload)

        ResponseAssertions.assert_ok(response)
        body = response.json()
        ResponseAssertions.assert_field_equals(body, "status", "sold")

    def test_update_pet_with_form_data(self, pet_client: PetClient, created_pet: dict):
        pet_id = created_pet["id"]
        response = pet_client.update_pet_with_form(pet_id, name="FormUpdated", status="pending")

        ResponseAssertions.assert_ok(response)


class TestPetDelete:
    """Tests for DELETE /pet/{id}"""

    def test_delete_pet_returns_200(self, pet_client: PetClient, new_pet_payload: dict):
        create_resp = pet_client.add_pet(new_pet_payload)
        assert create_resp.status_code == 200
        pet_id = create_resp.json()["id"]

        delete_resp = pet_client.delete_pet(pet_id)
        ResponseAssertions.assert_ok(delete_resp)

    def test_deleted_pet_is_no_longer_found(self, pet_client: PetClient, new_pet_payload: dict):
        create_resp = pet_client.add_pet(new_pet_payload)
        assert create_resp.status_code == 200
        pet_id = create_resp.json()["id"]

        pet_client.delete_pet(pet_id)
        get_resp = pet_client.get_pet_by_id(pet_id)

        ResponseAssertions.assert_not_found(get_resp)