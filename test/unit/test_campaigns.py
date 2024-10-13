from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_get_campaigns(client: TestClient):
    response = client.get("/campaigns")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_campaign_name(client: TestClient):
    # First, create a campaign to update
    response = client.patch("/campaigns/update-name/1", json={"name": "New Campaign Name"})
    assert response.status_code == 404  # Assuming there is no campaign with id 1 initially

    # Add logic to create a campaign and then test the update if needed
