import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
from unittest import mock

client = TestClient(app)


# Mock PostgreSQL DB interaction
def mock_pg_connection_get_data(query, params):
    return [
        {"device_id": "00:14:22:01:23:45", "device_type": "security_camera", "event_type": "motion_detected"}
    ]  # Return mocked event data


def test_get_events_invalid_query_params():
    response = client.get("/events?invalid_param=test")
    assert response.status_code == 400
    assert "Invalid query parameters" in response.json()["detail"]
