"""Assembly tests — routes, services, and repositories wired together.

These prove the layers actually connect and that domain errors surface as the
right HTTP status. External boundaries stay mocked or in-memory.
"""

from fastapi.testclient import TestClient


def test_health_reports_ok(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_then_read_item(client: TestClient):
    created = client.post("/items/", json={"name": "Acme"})
    assert created.status_code == 201
    item_id = created.json()["id"]

    fetched = client.get(f"/items/{item_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Acme"
    assert fetched.json()["status"] == "draft"


def test_get_unknown_item_returns_404(client: TestClient):
    assert client.get("/items/does-not-exist").status_code == 404


def test_blank_name_is_rejected(client: TestClient):
    assert client.post("/items/", json={"name": ""}).status_code == 422


def test_illegal_status_transition_returns_400(client: TestClient):
    item_id = client.post("/items/", json={"name": "Acme"}).json()["id"]
    client.patch(f"/items/{item_id}/status", json={"status": "archived"})

    response = client.patch(f"/items/{item_id}/status", json={"status": "ready"})
    assert response.status_code == 400
    assert "Cannot move" in response.json()["detail"]


def test_delete_removes_the_item(client: TestClient):
    item_id = client.post("/items/", json={"name": "Acme"}).json()["id"]

    assert client.delete(f"/items/{item_id}").status_code == 204
    assert client.get(f"/items/{item_id}").status_code == 404
