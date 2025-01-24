import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock
from cache.redis_cache import RedisCache

class TestRedisCache(unittest.TestCase):
    def setUp(self):
        self.redis_cache = RedisCache("localhost", 6379, 0)
        self.redis_cache.redis_client = MagicMock()

    def test_validate_user(self):
        self.redis_cache.redis_client.get.return_value = '{"is_authorized": true}'
        result = self.redis_cache.validate_user("user123")
        self.assertTrue(result)

    def test_add_validated_user(self):
        self.redis_cache.add_validated_user("user123")
        self.redis_cache.redis_client.set.assert_called_once_with("user123", '{"is_authorized": true}')