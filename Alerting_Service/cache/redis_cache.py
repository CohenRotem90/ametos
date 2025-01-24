import redis
import json


class RedisCache:
    def __init__(self, host, port, db):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def validate_user(self, user_id) -> bool:
        key = user_id
        retrieved_data = self.redis_client.get(key)
        if retrieved_data:
            return True
        return False

    def add_validated_user(self, user_id: str):
        key = user_id
        data = {"is_authorized": True}
        self.redis_client.set(key, json.dumps(data))
