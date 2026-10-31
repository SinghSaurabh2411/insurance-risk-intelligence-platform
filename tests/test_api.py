"""API route contract and security tests using mocked Oracle connections."""
import pytest
from fastapi.testclient import TestClient

from api.main import app
from api import main as main_module
from api.routers import channels, customers, dashboard, policies, products, yearly
from api.security import get_cors_origins

client = TestClient(app)
AUTH = {"X-API-Key": "test-secret"}


class FakeCursor:
    def __init__(self, row=None, rows=None, error=None):
        self.row, self.rows, self.error = row, rows or [], error

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def execute(self, *_args, **_kwargs):
        if self.error:
            raise self.error

    def fetchone(self):
        return self.row

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self, row=None, rows=None, error=None):
        self.cursor_obj = FakeCursor(row, rows, error)
        self.closed = False

    def cursor(self):
        return self.cursor_obj

    def close(self):
        self.closed = True


@pytest.fixture(autouse=True)
def configured_key(monkeypatch):
    monkeypatch.setenv("API_ACCESS_KEY", "test-secret")


@pytest.mark.parametrize("path", [
    "/health/db", "/dashboard/summary", "/dashboard/yearly",
    "/dashboard/products", "/dashboard/channels", "/dashboard/policies",
    "/dashboard/customers", "/dashboard/customer-cohorts",
])
def test_protected_routes_reject_missing_key(path):
    assert client.get(path).status_code == 401


def test_health_is_public():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_wrong_key_rejected():
    assert client.get("/dashboard/summary", headers={"X-API-Key": "wrong"}).status_code == 401


def test_missing_server_key_fails_closed(monkeypatch):
    monkeypatch.delenv("API_ACCESS_KEY")
    assert client.get("/dashboard/summary", headers=AUTH).status_code == 503


@pytest.mark.parametrize("path,module,row,rows,wrapper", [
    ("/dashboard/summary", dashboard,
     (45162, 228711, 194864832.6043, 134405079.5435, 852.0133819724456, 213938.16884281), None, None),
    ("/dashboard/yearly", yearly, None, [(2019, 10, 5, 100.0, 40.0, 10.0, 3.0)], "years"),
    ("/dashboard/products", products, None, [("P", "Y", 10, 5, 100.0, 40.0, 10.0, 3.0)], "products"),
    ("/dashboard/channels", channels, None, [("A", 10, 5, 100.0, 40.0, 10.0, 3.0)], "channels"),
    ("/dashboard/policies", policies, None, [("C", "C1", 10, 5, 100.0, 40.0, 10.0, 3.0)], "policies"),
    ("/dashboard/customers", customers, None, [("F", 10, 7, 5, 100.0, 40.0, 10.0, 3.0)], "customers"),
    ("/dashboard/customer-cohorts", customers, None, [(2000, 10, 7, 5, 100.0, 40.0, 10.0, 3.0)], "customer_cohorts"),
])
def test_analytics_endpoint_success(monkeypatch, path, module, row, rows, wrapper):
    connection = FakeConnection(row=row, rows=rows)
    monkeypatch.setattr(module, "get_api_connection", lambda: connection)
    response = client.get(path, headers=AUTH)
    assert response.status_code == 200, response.text
    body = response.json()
    if wrapper:
        assert wrapper in body and len(body[wrapper]) == 1
    else:
        assert body["total_policies"] == 45162
        assert body["total_observations"] == 228711
    assert connection.closed


def test_database_health_success(monkeypatch):
    connection = FakeConnection(row=(1,))
    monkeypatch.setattr(main_module, "get_api_connection", lambda: connection)
    response = client.get("/health/db", headers=AUTH)
    assert response.status_code == 200
    assert response.json()["connection"] == "successful"
    assert connection.closed


def test_database_health_failure_returns_503(monkeypatch):
    connection = FakeConnection(error=RuntimeError("database unavailable"))
    monkeypatch.setattr(main_module, "get_api_connection", lambda: connection)
    response = client.get("/health/db", headers=AUTH)
    assert response.status_code == 503
    assert connection.closed


def test_summary_database_failure_returns_503(monkeypatch):
    connection = FakeConnection(error=RuntimeError("database unavailable"))
    monkeypatch.setattr(dashboard, "get_api_connection", lambda: connection)
    response = client.get("/dashboard/summary", headers=AUTH)
    assert response.status_code == 503
    assert connection.closed


def test_cors_origins_parse_and_deduplicate(monkeypatch):
    monkeypatch.setenv("API_CORS_ORIGINS", "https://a.example, https://b.example,https://a.example")
    assert get_cors_origins() == ["https://a.example", "https://b.example"]


def test_cors_disallows_wildcard(monkeypatch):
    monkeypatch.setenv("API_CORS_ORIGINS", "https://a.example,*")
    with pytest.raises(ValueError):
        get_cors_origins()


def test_cors_defaults_to_empty(monkeypatch):
    monkeypatch.delenv("API_CORS_ORIGINS", raising=False)
    assert get_cors_origins() == []
