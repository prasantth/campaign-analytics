from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_performance_time_series(client: TestClient):
    response = client.get("/performance-time-series?aggregate_by=day&start_date=2024-01-01&end_date=2024-01-31")
    assert response.status_code == 200
    assert "data" in response.json()
    # Verify the structure of the data
    assert isinstance(response.json()["data"], list)

def test_compare_performance_preceding(client: TestClient):
    response = client.get(
        "/compare-performance?start_date=2024-01-01&end_date=2024-01-10&compare_mode=preceding"
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "current_period" in response_data
    assert "before_period" in response_data
    assert "comparison" in response_data
    # Further checks on the structure and values can be done here

def test_compare_performance_invalid_mode(client: TestClient):
    response = client.get(
        "/compare-performance?start_date=2024-01-01&end_date=2024-01-10&compare_mode=invalid_mode"
    )
    assert response.status_code == 422  # Unprocessable Entity
