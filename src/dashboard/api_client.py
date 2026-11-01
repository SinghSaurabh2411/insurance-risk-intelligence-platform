"""Reusable HTTP client for the Insurance Risk Intelligence API."""

from typing import Any

import httpx

from dashboard.config import get_api_access_key, get_api_base_url


class DashboardAPIError(Exception):
    """Raised when the dashboard cannot retrieve valid API data."""


class DashboardAPIClient:
    """Server-side client for the seven existing analytics endpoints."""

    TIMEOUT = 15.0
    ENDPOINTS = {
        "summary": "/dashboard/summary",
        "yearly": "/dashboard/yearly",
        "products": "/dashboard/products",
        "channels": "/dashboard/channels",
        "policies": "/dashboard/policies",
        "customers": "/dashboard/customers",
        "customer_cohorts": "/dashboard/customer-cohorts",
    }

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = TIMEOUT,
        transport: Any = None,
    ) -> None:
        self.base_url = (base_url or get_api_base_url()).rstrip("/")
        self.api_key = api_key or get_api_access_key()
        self.timeout = timeout
        self.transport = transport

    def _get(self, endpoint: str) -> dict:
        """Execute an authenticated GET request and validate its response."""
        try:
            with httpx.Client(timeout=self.timeout, transport=self.transport) as client:
                response = client.get(
                    f"{self.base_url}{endpoint}",
                    headers={"X-API-Key": self.api_key},
                )
            if response.status_code == 401:
                raise DashboardAPIError(
                    "API authentication failed. Check API_ACCESS_KEY."
                )
            if response.status_code == 503:
                raise DashboardAPIError(
                    "The API service or its database is unavailable."
                )
            response.raise_for_status()
            try:
                data = response.json()
            except ValueError as exc:
                raise DashboardAPIError(
                    "The API returned an invalid JSON response."
                ) from exc
            if not isinstance(data, dict):
                raise DashboardAPIError(
                    "The API returned an unexpected response format."
                )
            return data
        except DashboardAPIError:
            raise
        except httpx.TimeoutException as exc:
            raise DashboardAPIError(
                "The API request timed out. Please try again."
            ) from exc
        except httpx.ConnectError as exc:
            raise DashboardAPIError(
                "Cannot connect to the API. Check that the FastAPI service is running."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise DashboardAPIError(
                f"API request failed with HTTP {exc.response.status_code}."
            ) from exc
        except httpx.RequestError as exc:
            raise DashboardAPIError(
                "An unexpected network error occurred while contacting the API."
            ) from exc

    def get_summary(self) -> dict:
        return self._get(self.ENDPOINTS["summary"])

    def get_yearly(self) -> dict:
        return self._get(self.ENDPOINTS["yearly"])

    def get_products(self) -> dict:
        return self._get(self.ENDPOINTS["products"])

    def get_channels(self) -> dict:
        return self._get(self.ENDPOINTS["channels"])

    def get_policies(self) -> dict:
        return self._get(self.ENDPOINTS["policies"])

    def get_customers(self) -> dict:
        return self._get(self.ENDPOINTS["customers"])

    def get_customer_cohorts(self) -> dict:
        return self._get(self.ENDPOINTS["customer_cohorts"])
