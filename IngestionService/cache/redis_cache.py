import redis
import json
from fastapi import HTTPException
from models.models import SensorModel


class RedisCache:
    def __init__(self, host, port, db):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def is_device_in_cache(self, device_id):
        key = f"event:{device_id}"
        retrieved_data = self.redis_client.get(key)
        if retrieved_data:
            return json.loads(retrieved_data)["is_valid"]
        return None

    def add_device(self, event: SensorModel, is_valid_id):
        key = f"event:{event.device_id}"
        # not all event
        data = event.__dict__
        data["is_valid"] = is_valid_id
        self.redis_client.set(key, json.dumps(data))
        if not is_valid_id:
            raise HTTPException(status_code=400, detail="device_id not valid")
