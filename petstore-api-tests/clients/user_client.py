import requests
from clients.base_client import BaseClient


class UserClient(BaseClient):
    """
    Service Object for the /user endpoint group.
    Encapsulates all user-related API interactions.
    """

    ENDPOINT = "/user"

    def create_user(self, payload: dict) -> requests.Response:
        """POST /user — Create a new user."""
        return self.post(self.ENDPOINT, payload)

    def create_users_with_list(self, users: list) -> requests.Response:
        """POST /user/createWithList — Creates users with a list."""
        return self.post(f"{self.ENDPOINT}/createWithList", users)

    def login(self, username: str, password: str) -> requests.Response:
        """GET /user/login — Logs user into the system."""
        return self.get(f"{self.ENDPOINT}/login", params={"username": username, "password": password})

    def logout(self) -> requests.Response:
        """GET /user/logout — Logs out current logged-in user session."""
        return self.get(f"{self.ENDPOINT}/logout")

    def get_user(self, username: str) -> requests.Response:
        """GET /user/{username} — Get user by username."""
        return self.get(f"{self.ENDPOINT}/{username}")

    def update_user(self, username: str, payload: dict) -> requests.Response:
        """PUT /user/{username} — Updated user."""
        return self.put(f"{self.ENDPOINT}/{username}", payload)

    def delete_user(self, username: str) -> requests.Response:
        """DELETE /user/{username} — Delete user."""
        return self.delete(f"{self.ENDPOINT}/{username}")
