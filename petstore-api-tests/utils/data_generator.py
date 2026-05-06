import random
import string
import time


class DataGenerator:
    """Utility for generating unique test data to avoid conflicts between test runs."""

    @staticmethod
    def unique_id() -> int:
        """Generate a unique numeric ID based on current timestamp."""
        return int(time.time() * 1000) % 999999 + random.randint(1, 100)

    @staticmethod
    def random_string(length: int = 8) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def unique_username() -> str:
        return f"user_{DataGenerator.random_string(6)}_{int(time.time()) % 10000}"

    @staticmethod
    def unique_email(username: str) -> str:
        return f"{username}@testmail.com"

    @staticmethod
    def pet_status() -> list:
        return ["available", "pending", "sold"]
