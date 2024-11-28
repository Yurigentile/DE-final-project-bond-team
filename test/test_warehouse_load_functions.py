import boto3
import json
from moto import mock_aws
import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from lambda_load.src.warehouse_load_functions import get_secret, alchemy_db_connection, alchemy_close_connection, load_data_into_warehouse

@mock_aws
class TestGetSecret(unittest.TestCase):
    def setUp(self):
        # Set up a mock AWS Secrets Manager
        self.client = boto3.client("secretsmanager", region_name = 'eu-west-2')
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
    
    @patch("lambda_load.src.warehouse_load_functions.boto3.client")
    def test_get_secret_client_error(self, mock_boto_client):
        # Test AWS ClientError        
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "Secret not found"}},
            "GetSecretValue",
        )
        
        result = get_secret("non-existent-secret")
        self.assertIsNone(result, "Should return None on ClientError")

    @patch("lambda_load.src.warehouse_load_functions.boto3.client")
    def test_get_secret_unexpected_error(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.get_secret_value.side_effect = Exception("Unexpected error")
        
        result = get_secret("some-secret")
        self.assertIsNone(result, "Should return None on unexpected error")

class TestAlchemyDBConnection(unittest.TestCase):
    @patch('lambda_load.src.warehouse_load_functions.get_secret')
    @patch('lambda_load.src.warehouse_load_functions.create_engine')
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

    @patch('lambda_load.src.warehouse_load_functions.get_secret')
    def test_alchemy_db_connection_no_secret(self, mock_get_secret):
        # Simulate get_secret returning None or empty string
        mock_get_secret.return_value = None
        
        with self.assertRaises(ValueError) as context:
            alchemy_db_connection('test_secret')
        
        self.assertTrue('Could not retrieve credentials' in str(context.exception))

    @patch('lambda_load.src.warehouse_load_functions.get_secret')
    @patch('lambda_load.src.warehouse_load_functions.create_engine')
    def test_alchemy_db_connection_failure(self, mock_create_engine, mock_get_secret):
        # Simulate failure in connection (engine.create throws an error)
        mock_get_secret.return_value = '{"username": "test_user", "password": "test_pass", "host": "localhost", "port": 5432, "dbname": "test_db"}'
        mock_create_engine.side_effect = Exception("Connection error")

        with self.assertRaises(Exception) as context:
            alchemy_db_connection('test_secret')

        self.assertTrue('Connection error' in str(context.exception))

class TestAlchemyCloseConnection(unittest.TestCase):    
    def setUp(self):
        # Create a mock engine
        self.mock_engine = MagicMock()
        self.logger = MagicMock()
    
    @patch('lambda_load.src.warehouse_load_functions.logger')
    def test_close_connection_success(self, mock_logger):
        # Create a mock engine
        mock_engine = MagicMock()
        mock_engine.dispose = MagicMock()
        
        # Call the function
        alchemy_close_connection(mock_engine)

        # Assert that dispose() was called on the engine
        mock_engine.dispose.assert_called_once()

        # Assert that logger.info was called with the expected message
        mock_logger.info.assert_called_with("Database connection engine closed")
    
    def test_close_connection_no_engine(self):
        # Test behavior when no engine is passed
        alchemy_close_connection(None)
        
        # Since no engine is provided, we expect dispose() not to be called
        self.mock_engine.dispose.assert_not_called()
    
    @patch('lambda_load.src.warehouse_load_functions.logger')
    def test_close_connection_exception(self, mock_logger):
        # Simulate an exception in dispose
        mock_engine = MagicMock()
        mock_engine.dispose.side_effect = Exception("Dispose failed")
        
        # Call the function
        alchemy_close_connection(mock_engine)
        
        # Check that the logger.error was called with the exception message
        mock_logger.error.assert_called_with("Error closing engine connection: Dispose failed")

class TestLoadDataIntoWarehouse(unittest.TestCase):
    @patch('lambda_load.src.warehouse_load_functions.alchemy_db_connection')
    @patch('lambda_load.src.warehouse_load_functions.logger')
    def test_load_data_into_warehouse_success(self, mock_logger, mock_db_connection):
        # Arrange
        db_params = {'host': 'localhost', 'user': 'user', 'password': 'password', 'database': 'test_db'}
        dataframes = {
            'table1': pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}),
            'table2': pd.DataFrame({'col1': [5, 6], 'col2': [7, 8]})
        }
        mock_engine = MagicMock()
        mock_db_connection.return_value = mock_engine
        
        # Mock the to_sql method of the DataFrame to avoid actual database operations
        with patch.object(pd.DataFrame, 'to_sql', return_value=None) as mock_to_sql:
            # Act
            load_data_into_warehouse(dataframes, db_params)
            
            # Assert that the to_sql method is called with the correct arguments
            mock_to_sql.assert_any_call(name='table1', con=mock_engine, schema='public', if_exists='append', index=False)
            mock_to_sql.assert_any_call(name='table2', con=mock_engine, schema='public', if_exists='append', index=False)
            
            # Assert logger calls for success
            mock_logger.info.assert_any_call("Loading table: table1 (Rows: 2)")
            mock_logger.info.assert_any_call("Successfully loaded table: table1")
            mock_logger.info.assert_any_call("Loading table: table2 (Rows: 2)")
            mock_logger.info.assert_any_call("Successfully loaded table: table2")

    @patch('lambda_load.src.warehouse_load_functions.alchemy_db_connection')
    @patch('lambda_load.src.warehouse_load_functions.logger')
    def test_load_data_into_warehouse_failure(self, mock_logger, mock_db_connection):
        # Arrange
        db_params = {'host': 'localhost', 'user': 'user', 'password': 'password', 'database': 'test_db'}
        dataframes = {
            'table1': pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}),
            'table2': pd.DataFrame({'col1': [5, 6], 'col2': [7, 8]})
        }
        mock_engine = MagicMock()
        mock_db_connection.return_value = mock_engine
        
        # Simulate an exception during the loading of the DataFrame
        with patch.object(pd.DataFrame, 'to_sql', side_effect=Exception("Database error")):
            # Act
            load_data_into_warehouse(dataframes, db_params)
            
            # Assert that the logger recorded the error
            mock_logger.error.assert_any_call("Failed to load table table1: Database error")
            mock_logger.error.assert_any_call("Failed to load table table2: Database error")              

if __name__ == "__main__":
    unittest.main()