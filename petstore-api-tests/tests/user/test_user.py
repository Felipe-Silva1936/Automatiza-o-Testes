"""
Test Suite: User Endpoints
Covers: POST /user, POST /user/createWithList, GET /user/login,
        GET /user/logout, GET /user/{username},
        PUT /user/{username}, DELETE /user/{username}
"""
import pytest
from clients import UserClient
from models import UserBuilder
from utils import ResponseAssertions, DataGenerator


class TestUserCreate:
    """Tests for POST /user"""

    def test_create_user_returns_200(self, user_client: UserClient, new_user_payload: dict):
        response = user_client.create_user(new_user_payload)

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_content_type_json(response)
        # Cleanup
        user_client.delete_user(new_user_payload["username"])

    def test_create_user_response_contains_message(self, user_client: UserClient, new_user_payload: dict):
        response = user_client.create_user(new_user_payload)
        body = response.json()

        ResponseAssertions.assert_ok(response)
        assert "message" in body or "code" in body, "Response should contain 'message' or 'code'"
        # Cleanup
        user_client.delete_user(new_user_payload["username"])

    def test_create_users_with_list_returns_200(self, user_client: UserClient):
        users = [
            UserBuilder()
            .with_id(DataGenerator.unique_id())
            .with_username(DataGenerator.unique_username())
            .with_name("Test", "Batch")
            .with_email("batch@test.com")
            .with_password("pass123")
            .build()
            .to_dict()
            for _ in range(3)
        ]

        response = user_client.create_users_with_list(users)
        ResponseAssertions.assert_ok(response)

        # Cleanup
        for user in users:
            user_client.delete_user(user["username"])


class TestUserAuth:
    """Tests for GET /user/login and GET /user/logout"""

    def test_login_with_valid_credentials_returns_200(self, user_client: UserClient, created_user: dict):
        response = user_client.login(created_user["username"], created_user["password"])

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_content_type_json(response)

    def test_login_response_contains_session_token(self, user_client: UserClient, created_user: dict):
        response = user_client.login(created_user["username"], created_user["password"])
        body = response.json()

        ResponseAssertions.assert_ok(response)
        assert "message" in body, "Login response should contain 'message' (session token)"
        assert len(body["message"]) > 0, "Session token should not be empty"

    def test_login_sets_rate_limit_header(self, user_client: UserClient, created_user: dict):
        response = user_client.login(created_user["username"], created_user["password"])

        ResponseAssertions.assert_ok(response)
        assert "X-Rate-Limit" in response.headers or "x-rate-limit" in response.headers, (
            "Login response should include X-Rate-Limit header"
        )

    def test_login_sets_expiration_header(self, user_client: UserClient, created_user: dict):
        response = user_client.login(created_user["username"], created_user["password"])

        ResponseAssertions.assert_ok(response)
        assert "X-Expires-After" in response.headers or "x-expires-after" in response.headers, (
            "Login response should include X-Expires-After header"
        )

    def test_logout_returns_200(self, user_client: UserClient):
        response = user_client.logout()
        ResponseAssertions.assert_ok(response)


class TestUserRead:
    """Tests for GET /user/{username}"""

    def test_get_user_returns_200(self, user_client: UserClient, created_user: dict):
        response = user_client.get_user(created_user["username"])

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_content_type_json(response)

    def test_get_user_returns_correct_username(self, user_client: UserClient, created_user: dict):
        response = user_client.get_user(created_user["username"])
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "username", created_user["username"])

    def test_get_user_contains_required_fields(self, user_client: UserClient, created_user: dict):
        response = user_client.get_user(created_user["username"])
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_present(body, "id", "username", "firstName", "lastName", "email")

    def test_get_user_email_matches(self, user_client: UserClient, created_user: dict):
        response = user_client.get_user(created_user["username"])
        body = response.json()

        ResponseAssertions.assert_ok(response)
        ResponseAssertions.assert_field_equals(body, "email", created_user["email"])

    def test_get_nonexistent_user_returns_404(self, user_client: UserClient):
        response = user_client.get_user("userThatDoesNotExist_xyz999")

        ResponseAssertions.assert_not_found(response)


class TestUserUpdate:
    """Tests for PUT /user/{username}"""

    def test_update_user_returns_200(self, user_client: UserClient, created_user: dict):
        updated_payload = {**created_user, "firstName": "Updated"}
        response = user_client.update_user(created_user["username"], updated_payload)

        ResponseAssertions.assert_ok(response)

    def test_update_user_email(self, user_client: UserClient, created_user: dict):
        new_email = f"updated_{DataGenerator.random_string(4)}@test.com"
        updated_payload = {**created_user, "email": new_email}
        user_client.update_user(created_user["username"], updated_payload)

        # Verify the update
        get_response = user_client.get_user(created_user["username"])
        body = get_response.json()

        ResponseAssertions.assert_ok(get_response)
        ResponseAssertions.assert_field_equals(body, "email", new_email)


class TestUserDelete:
    """Tests for DELETE /user/{username}"""

    def test_delete_user_returns_200(self, user_client: UserClient, new_user_payload: dict):
        user_client.create_user(new_user_payload)
        response = user_client.delete_user(new_user_payload["username"])

        ResponseAssertions.assert_ok(response)

    def test_deleted_user_is_no_longer_found(self, user_client: UserClient, new_user_payload: dict):
        user_client.create_user(new_user_payload)
        user_client.delete_user(new_user_payload["username"])

        get_resp = user_client.get_user(new_user_payload["username"])
        ResponseAssertions.assert_not_found(get_resp)
