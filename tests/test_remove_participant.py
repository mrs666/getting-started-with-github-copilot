import pytest


@pytest.mark.asyncio
async def test_remove_success(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Ensure participant exists initially
    r = await client.get("/activities")
    assert email in r.json()[activity]["participants"]

    # Remove participant
    r = await client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 200
    assert "Removed" in r.json().get("message", "")

    # Ensure participant no longer present
    r = await client.get("/activities")
    assert email not in r.json()[activity]["participants"]


@pytest.mark.asyncio
async def test_remove_nonexistent_participant(client):
    activity = "Chess Club"
    email = "doesnotexist@example.com"
    r = await client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_remove_nonexistent_activity(client):
    r = await client.delete("/activities/NoSuchActivity/participants", params={"email": "a@b.com"})
    assert r.status_code == 404
