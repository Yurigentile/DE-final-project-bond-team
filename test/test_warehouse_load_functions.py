import boto3
import json
import unittest
from unittest.mock import patch, MagicMock
from moto import mock_aws
from botocore.exceptions import ClientError
from load_lambda.src.warehouse_load_functions import get_secret, alchemy_db_connection

@mock_aws
class TestGetSecret(unittest.TestCase):
    def setUp(self):
        # Set up a mock AWS Secrets Manager
        self.client = boto3.client("secretsmanager")
        self.secret_name = "test-secret"
        self.secret_value = {"username": "admin", "password": "password123"}
        self.client.create_secret(
            Name=self.secret_name,
            SecretString=json.dumps(self.secret_value),
        )
    
    def test_get_secret_success(self):
        # Test successful retrieval of the secret
        result = get_secret(self.secret_name)
        self.assertIsInstance(result, dict, "Secret should be a dictionary")
        self.assertEqual(result, self.secret_value, "Secret value does not match expected")

    def test_get_secret_not_found(self):
        # Test retrieving a non-existent secret
        result = get_secret("non-existent-secret")
        self.assertIsNone(result, "Should return None for non-existent secret")
    
    def test_get_secret_invalid_json(self):
        # Test when the secret is not valid JSON
        invalid_secret_name = "invalid-secret"
        self.client.create_secret(
            Name=invalid_secret_name,
            SecretString="not-a-json",
        )
        
        result = get_secret(invalid_secret_name)
        self.assertIsNone(result, "Should return None for invalid JSON")
    
    @patch("load_lambda.src.warehouse_load_functions.boto3.client")
    def test_get_secret_client_error(self, mock_boto_client):
        # Test AWS ClientError        
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "Secret not found"}},
            "GetSecretValue",
        )
        
        result = get_secret("non-existent-secret")
        self.assertIsNone(result, "Should return None on ClientError")

    @patch("load_lambda.src.warehouse_load_functions.boto3.client")
    def test_get_secret_unexpected_error(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.side_effect = Exception("Unexpected error")
        
        result = get_secret("some-secret")
        self.assertIsNone(result, "Should return None on unexpected error")

class TestAlchemyDBConnection(unittest.TestCase):
    @patch('load_lambda.src.warehouse_load_functions.get_secret')
    @patch('load_lambda.src.warehouse_load_functions.create_engine')
    def test_alchemy_db_connection_success(self, mock_create_engine, mock_get_secret):
        # Mock the secret retrieval and database engine creation
        mock_get_secret.return_value = '{"username": "test_user", "password": "test_pass", "host": "localhost", "port": 5432, "dbname": "test_db"}'
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        
        # Call the function
        result = alchemy_db_connection('test_secret')

        # Assertions
        mock_get_secret.assert_called_once_with('test_secret')
        mock_create_engine.assert_called_once_with('postgresql+psycopg2://test_user:test_pass@localhost:5432/test_db')
        mock_engine.connect.assert_called_once()
        self.assertEqual(result, mock_engine)

    @patch('load_lambda.src.warehouse_load_functions.get_secret')
    def test_alchemy_db_connection_no_secret(self, mock_get_secret):
        # Simulate get_secret returning None or empty string
        mock_get_secret.return_value = None
        
        with self.assertRaises(ValueError) as context:
            alchemy_db_connection('test_secret')
        
        self.assertTrue('Could not retrieve credentials' in str(context.exception))

    @patch('load_lambda.src.warehouse_load_functions.get_secret')
    @patch('load_lambda.src.warehouse_load_functions.create_engine')
    def test_alchemy_db_connection_failure(self, mock_create_engine, mock_get_secret):
        # Simulate failure in connection (engine.create throws an error)
        mock_get_secret.return_value = '{"username": "test_user", "password": "test_pass", "host": "localhost", "port": 5432, "dbname": "test_db"}'
        mock_create_engine.side_effect = Exception("Connection error")

        with self.assertRaises(Exception) as context:
            alchemy_db_connection('test_secret')

        self.assertTrue('Connection error' in str(context.exception))        

if __name__ == "__main__":
    unittest.main()