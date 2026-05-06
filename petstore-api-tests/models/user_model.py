from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    id: Optional[int] = None
    user_status: int = 0

    def to_dict(self) -> dict:
        payload = {
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "userStatus": self.user_status,
        }
        if self.id is not None:
            payload["id"] = self.id
        return payload


class UserBuilder:
    """
    Builder pattern for constructing User payloads with fluent interface.
    """

    def __init__(self):
        self._id: Optional[int] = None
        self._username: str = "testuser"
        self._first_name: str = "Test"
        self._last_name: str = "User"
        self._email: str = "test@example.com"
        self._password: str = "password123"
        self._phone: str = "11999999999"
        self._user_status: int = 0

    def with_id(self, user_id: int) -> "UserBuilder":
        self._id = user_id
        return self

    def with_username(self, username: str) -> "UserBuilder":
        self._username = username
        return self

    def with_name(self, first: str, last: str) -> "UserBuilder":
        self._first_name = first
        self._last_name = last
        return self

    def with_email(self, email: str) -> "UserBuilder":
        self._email = email
        return self

    def with_password(self, password: str) -> "UserBuilder":
        self._password = password
        return self

    def with_phone(self, phone: str) -> "UserBuilder":
        self._phone = phone
        return self

    def build(self) -> User:
        return User(
            id=self._id,
            username=self._username,
            first_name=self._first_name,
            last_name=self._last_name,
            email=self._email,
            password=self._password,
            phone=self._phone,
            user_status=self._user_status,
        )
