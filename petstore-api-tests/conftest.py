import pytest
from clients import PetClient, StoreClient, UserClient
from models import PetBuilder, UserBuilder, OrderBuilder
from utils import DataGenerator


# ──────────────────────────────────────────
# Client Fixtures
# ──────────────────────────────────────────

@pytest.fixture(scope="session")
def pet_client() -> PetClient:
    """Shared PetClient instance for the entire test session."""
    return PetClient()


@pytest.fixture(scope="session")
def store_client() -> StoreClient:
    """Shared StoreClient instance for the entire test session."""
    return StoreClient()


@pytest.fixture(scope="session")
def user_client() -> UserClient:
    """Shared UserClient instance for the entire test session."""
    return UserClient()


# ──────────────────────────────────────────
# Pet Fixtures
# ──────────────────────────────────────────

@pytest.fixture
def new_pet_payload() -> dict:
    """Generates a unique pet payload for each test."""
    pet_id = DataGenerator.unique_id()
    return (
        PetBuilder()
        .with_id(pet_id)
        .with_name(f"Pet_{DataGenerator.random_string(5)}")
        .with_status("available")
        .with_category(1, "Dogs")
        .with_tag(1, "friendly")
        .build()
        .to_dict()
    )


@pytest.fixture
def created_pet(pet_client: PetClient, new_pet_payload: dict) -> dict:
    """Creates a pet via API and returns the response body. Cleans up after test."""
    response = pet_client.add_pet(new_pet_payload)
    assert response.status_code == 200, f"Setup failed: could not create pet. Body: {response.text}"
    pet = response.json()
    yield pet
    # Teardown: remove the pet after each test
    pet_client.delete_pet(pet["id"])


# ──────────────────────────────────────────
# User Fixtures
# ──────────────────────────────────────────

@pytest.fixture
def new_user_payload() -> dict:
    """Generates a unique user payload for each test."""
    username = DataGenerator.unique_username()
    return (
        UserBuilder()
        .with_id(DataGenerator.unique_id())
        .with_username(username)
        .with_name("Test", "User")
        .with_email(DataGenerator.unique_email(username))
        .with_password("SecurePass123!")
        .with_phone("11999990000")
        .build()
        .to_dict()
    )


@pytest.fixture
def created_user(user_client: UserClient, new_user_payload: dict) -> dict:
    """Creates a user via API and returns the payload. Cleans up after test."""
    response = user_client.create_user(new_user_payload)
    assert response.status_code == 200, f"Setup failed: could not create user. Body: {response.text}"
    yield new_user_payload
    # Teardown: remove the user after each test
    user_client.delete_user(new_user_payload["username"])


# ──────────────────────────────────────────
# Order Fixtures
# ──────────────────────────────────────────

@pytest.fixture
def new_order_payload() -> dict:
    """Generates a unique order payload for each test."""
    return (
        OrderBuilder()
        .with_id(DataGenerator.unique_id() % 10 + 1)  # Petstore accepts 1-10 only
        .with_pet_id(DataGenerator.unique_id())
        .with_quantity(2)
        .with_status("placed")
        .build()
        .to_dict()
    )


@pytest.fixture
def created_order(store_client: StoreClient, new_order_payload: dict) -> dict:
    """Places an order via API and returns the response body. Cleans up after test."""
    response = store_client.place_order(new_order_payload)
    assert response.status_code == 200, f"Setup failed: could not create order. Body: {response.text}"
    order = response.json()
    yield order
    store_client.delete_order(order["id"])
