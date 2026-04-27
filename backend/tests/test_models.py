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
    assert data["page"] == 1
    assert data["pages"] == 0


@pytest.mark.asyncio
async def test_create_model(client: AsyncClient, admin_headers: dict):
    response = await client.post("/api/v1/models/", json=SAMPLE_MODEL, headers=admin_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Model"
    assert data["provider"] == "TestProvider"
    assert data["id"] == 1
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_model_unauthorized(client: AsyncClient):
    response = await client.post("/api/v1/models/", json=SAMPLE_MODEL)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_model_wrong_key(client: AsyncClient):
    response = await client.post("/api/v1/models/", json=SAMPLE_MODEL, headers={"X-API-Key": "wrong"})
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_and_list_model(client: AsyncClient, admin_headers: dict):
    await client.post("/api/v1/models/", json=SAMPLE_MODEL, headers=admin_headers)
    response = await client.get("/api/v1/models/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert data["pages"] == 1
    assert data["models"][0]["name"] == "Test Model"


@pytest.mark.asyncio
async def test_get_model_by_id(client: AsyncClient, admin_headers: dict):
    create_resp = await client.post("/api/v1/models/", json=SAMPLE_MODEL, headers=admin_headers)
    model_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Model"


@pytest.mark.asyncio
async def test_create_model_missing_fields(client: AsyncClient, admin_headers: dict):
    response = await client.post("/api/v1/models/", json={"name": "Incomplete"}, headers=admin_headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_filter_by_provider(client: AsyncClient, admin_headers: dict):
    await client.post("/api/v1/models/", json=SAMPLE_MODEL, headers=admin_headers)
    await client.post("/api/v1/models/", json={**SAMPLE_MODEL, "name": "Other Model", "provider": "OtherProvider"}, headers=admin_headers)

    response = await client.get("/api/v1/models/?provider=TestProvider")
    data = response.json()
    assert data["total"] == 1
    assert data["models"][0]["provider"] == "TestProvider"


@pytest.mark.asyncio
async def test_sort_by_price_desc(client: AsyncClient, admin_headers: dict):
    await client.post("/api/v1/models/", json={**SAMPLE_MODEL, "name": "Cheap", "input_price": 0.5}, headers=admin_headers)
    await client.post("/api/v1/models/", json={**SAMPLE_MODEL, "name": "Expensive", "input_price": 10.0}, headers=admin_headers)

    response = await client.get("/api/v1/models/?sort_by=input_price&order=desc")
    data = response.json()
    assert data["models"][0]["name"] == "Expensive"
    assert data["models"][1]["name"] == "Cheap"


@pytest.mark.asyncio
async def test_pagination(client: AsyncClient, admin_headers: dict):
    for i in range(5):
        await client.post("/api/v1/models/", json={**SAMPLE_MODEL, "name": f"Model {i}"}, headers=admin_headers)

    response = await client.get("/api/v1/models/?page=1&per_page=2")
    data = response.json()
    assert data["total"] == 5
    assert data["pages"] == 3
    assert data["page"] == 1
    assert len(data["models"]) == 2
