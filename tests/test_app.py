import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["service"] == "observability-demo"


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_metrics():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"demo_http_requests_total" in response.data
