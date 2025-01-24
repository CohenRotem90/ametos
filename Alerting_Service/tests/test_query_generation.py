import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from database.postgreSQL_db import PostgreSQL_db

class TestQueryGeneration(unittest.TestCase):
    def test_get_query_syntax_and_params(self):
        query, params = PostgreSQL_db.get_query_syntax_and_params(device_id="123", device_type="radar")
        self.assertEqual(query, "SELECT * FROM alerts WHERE 1=1 AND device_id = %s AND device_type = %s")
        self.assertEqual(params, ["123", "radar"])