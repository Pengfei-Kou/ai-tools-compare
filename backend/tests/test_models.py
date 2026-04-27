import pytest
from httpx import AsyncClient

SAMPLE_MODEL = {
    "name": "Test Model",
    "provider": "TestProvider",
    "description": "A test model",
    "input_price": 1.0,
    "output_price": 5.0,
    "context_window": 128000,
    "category": "chat",
}


@pytest.mark.asyncio
async def test_list_models_empty(client: AsyncClient):
    response = await client.get("/api/v1/models/")
    assert response.status_code == 200
    data = response.json()
    assert data["models"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_create_model(client: AsyncClient):
    response = await client.post("/api/v1/models/", json=SAMPLE_MODEL)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Model"
    assert data["provider"] == "TestProvider"
    assert data["id"] == 1
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_and_list_model(client: AsyncClient):
    await client.post("/api/v1/models/", json=SAMPLE_MODEL)
    response = await client.get("/api/v1/models/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["models"][0]["name"] == "Test Model"


@pytest.mark.asyncio
async def test_get_model_by_id(client: AsyncClient):
    create_resp = await client.post("/api/v1/models/", json=SAMPLE_MODEL)
    model_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Model"


@pytest.mark.asyncio
async def test_create_model_missing_fields(client: AsyncClient):
    response = await client.post("/api/v1/models/", json={"name": "Incomplete"})
    assert response.status_code == 422
