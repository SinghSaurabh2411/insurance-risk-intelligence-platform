"""Tests for the Streamlit dashboard API client."""

import httpx
import pytest

from dashboard.api_client import DashboardAPIClient, DashboardAPIError


@pytest.fixture
def client():
    return DashboardAPIClient(base_url="http://test-api", api_key="test-key")


@pytest.mark.parametrize(
    "method,endpoint,payload",
    [
        ("get_summary", "/dashboard/summary", {"total_policies": 45162}),
        ("get_yearly", "/dashboard/yearly", {"years": []}),
        ("get_products", "/dashboard/products", {"products": []}),
        ("get_channels", "/dashboard/channels", {"channels": []}),
        ("get_policies", "/dashboard/policies", {"policies": []}),
        ("get_customers", "/dashboard/customers", {"customers": []}),
        ("get_customer_cohorts", "/dashboard/customer-cohorts", {"customer_cohorts": []}),
    ],
)
def test_analytics_endpoints(client, method, endpoint, payload):
    def handler(request):
        assert request.url.path == endpoint
        assert request.headers["X-API-Key"] == "test-key"
        return httpx.Response(200, json=payload)

    client.transport = httpx.MockTransport(handler)
    assert getattr(client, method)() == payload


def test_invalid_api_key(client):
    client.transport = httpx.MockTransport(
        lambda request: httpx.Response(401, json={"detail": "Invalid API key."})
    )
    with pytest.raises(DashboardAPIError, match="authentication failed"):
        client.get_summary()


def test_api_unavailable(client):
    client.transport = httpx.MockTransport(
        lambda request: httpx.Response(503, json={"detail": "Unavailable"})
    )
    with pytest.raises(DashboardAPIError, match="unavailable"):
        client.get_summary()


def test_api_connection_error(client):
    def handler(request):
        raise httpx.ConnectError("Connection refused")

    client.transport = httpx.MockTransport(handler)
    with pytest.raises(DashboardAPIError, match="Cannot connect"):
        client.get_summary()


def test_invalid_json_response(client):
    client.transport = httpx.MockTransport(
        lambda request: httpx.Response(200, text="not-json")
    )
    with pytest.raises(DashboardAPIError, match="invalid JSON"):
        client.get_summary()


def test_unexpected_response_format(client):
    client.transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json=[])
    )
    with pytest.raises(DashboardAPIError, match="unexpected response format"):
        client.get_summary()
