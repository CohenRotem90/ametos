import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_post_event():
    # Create a sample event object for testing
    event_data = {
        "device_id": "11:22:33:44:55:66",
        "timestamp": "2024-12-18T14:10:00Z",
        "event_type": "speed_violation",
        "speed_kmh": 70,
        "location": "Zone A"
    }

    # Post the event to the API
    response = client.post("/events", json=event_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Event handled successfully"}
