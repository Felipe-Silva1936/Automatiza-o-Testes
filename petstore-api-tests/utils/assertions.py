import requests


class ResponseAssertions:
    """
    Assertion helper following the Helper Object pattern.
    Centralizes common API response validations for reuse across tests.
    """

    @staticmethod
    def assert_status_code(response: requests.Response, expected: int) -> None:
        assert response.status_code == expected, (
            f"Expected status {expected}, got {response.status_code}. "
            f"Body: {response.text}"
        )

    @staticmethod
    def assert_ok(response: requests.Response) -> None:
        ResponseAssertions.assert_status_code(response, 200)

    @staticmethod
    def assert_created(response: requests.Response) -> None:
        ResponseAssertions.assert_status_code(response, 200)  # Petstore returns 200 on create

    @staticmethod
    def assert_not_found(response: requests.Response) -> None:
        ResponseAssertions.assert_status_code(response, 404)

    @staticmethod
    def assert_content_type_json(response: requests.Response) -> None:
        assert "application/json" in response.headers.get("Content-Type", ""), (
            f"Expected JSON content-type, got: {response.headers.get('Content-Type')}"
        )

    @staticmethod
    def assert_response_time(response: requests.Response, max_seconds: float = 3.0) -> None:
        elapsed = response.elapsed.total_seconds()
        assert elapsed <= max_seconds, (
            f"Response too slow: {elapsed:.2f}s (max {max_seconds}s)"
        )

    @staticmethod
    def assert_field_equals(body: dict, field: str, expected) -> None:
        assert field in body, f"Field '{field}' not found in response body"
        assert body[field] == expected, (
            f"Field '{field}': expected '{expected}', got '{body[field]}'"
        )

    @staticmethod
    def assert_field_present(body: dict, *fields: str) -> None:
        for field in fields:
            assert field in body, f"Required field '{field}' missing from response"

    @staticmethod
    def assert_list_not_empty(response: requests.Response) -> list:
        body = response.json()
        assert isinstance(body, list), f"Expected list, got {type(body)}"
        assert len(body) > 0, "Expected non-empty list, but got empty"
        return body
