import pytest


@pytest.mark.asyncio
async def test_get_activities(client):
    response = await client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # Basic assertions about structure
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)
