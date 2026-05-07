import requests
from config.settings import settings


class BaseClient:
    """
    Base HTTP client following the Service Object pattern.
    Centralizes request configuration, headers, and response handling.
    """

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.timeout = settings.TIMEOUT
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params, timeout=self.timeout)

    def post(self, endpoint: str, payload: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=payload, timeout=self.timeout)

    def put(self, endpoint: str, payload: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.put(url, json=payload, timeout=self.timeout)

    def delete(self, endpoint: str) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url, timeout=self.timeout)

    def post_form(self, endpoint: str, data: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.session.post(url, data=data, headers=headers, timeout=self.timeout)
