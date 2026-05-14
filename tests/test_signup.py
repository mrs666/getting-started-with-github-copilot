import pytest


@pytest.mark.asyncio
async def test_signup_success(client):
    email = "tester@example.com"
    activity = "Chess Club"

    # Ensure not present initially
    r = await client.get("/activities")
    assert email not in r.json()[activity]["participants"]

    # Signup
    r = await client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Ensure participant now appears
    r = await client.get("/activities")
    assert email in r.json()[activity]["participants"]


@pytest.mark.asyncio
async def test_signup_duplicate(client):
    email = "dup@example.com"
    activity = "Chess Club"

    # First signup should succeed
    r = await client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200

    # Second signup should fail with 400
    r = await client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_signup_nonexistent_activity(client):
    r = await client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert r.status_code == 404
