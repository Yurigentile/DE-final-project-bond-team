from extract_lambda.src.db_connection import create_conn
import json
import unittest


class TestDBConnection(unittest.TestCase):
    def test_function_raises_pg8000_errors(self):
        secret_value = {
            "cohort_id": "de_2024_09_02",
            "host": "rds.com",
            "user": "alpha",
            "password": "beta",
            "database": "gamma",
            "port": 5432,
        }

        with self.assertRaises(Exception) as detail:
            create_conn(json.dumps(secret_value))
            self.assertEqual(str(detail.exception))
