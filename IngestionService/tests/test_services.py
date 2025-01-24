import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

from unittest import mock
from cache.redis_cache import RedisCache
from database.postgreSQL_db import PostgreSQL_db
from models.models import SensorModel


def test_redis_is_device_in_cache():
    redis_service = RedisCache(host="localhost", port=6379, db=0)

    # Mocking Redis behavior
    with mock.patch.object(redis_service, 'is_device_in_cache', return_value=None):
        result = redis_service.is_device_in_cache("00:14:22:01:23:45")

    assert result is None  # Device not in cache


def test_pg_send_data():
    pg_service = PostgreSQL_db(dbname="ametos", user="postgres", password="postgres", host="localhost", port=5432)

    # Mocking the database interaction
    with mock.patch.object(pg_service, 'send_data') as mock_send:
        event = SensorModel(device_id="00:14:22:01:23:45", device_type="security_camera")
        pg_service.send_data(event)

        mock_send.assert_called_once_with(event)