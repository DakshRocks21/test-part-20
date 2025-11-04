import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_create_note(client):
    response = client.post("/notes", json={"content": "Test note"})
    assert response.status_code == 201
    assert "id" in response.json


def test_healthcheck(client):
    response = client.get("/health")
    assert response.json == {"status": "ok"}
