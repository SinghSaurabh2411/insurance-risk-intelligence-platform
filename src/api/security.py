"""API-key authentication and strict CORS configuration."""
import hmac
import os
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(api_key: str | None = Security(api_key_header)) -> None:
    expected = os.getenv("API_ACCESS_KEY", "").strip()
    if not expected:
        raise HTTPException(status_code=503, detail="API authentication is not configured.")
    if not api_key or not hmac.compare_digest(api_key, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

def get_cors_origins() -> list[str]:
    raw = os.getenv("API_CORS_ORIGINS", "")
    origins = list(dict.fromkeys(value.strip() for value in raw.split(",") if value.strip()))
    if "*" in origins:
        raise ValueError("Wildcard CORS origins are not permitted.")
    return origins
