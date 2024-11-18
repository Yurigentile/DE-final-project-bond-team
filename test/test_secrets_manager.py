import pytest
from unittest.mock import patch, Mock
import json
from botocore.exceptions import ClientError
from extract_lambda.src.secrets_manager import get_secret

def test_get_secret_find_secret():
    # Create mock secret value
    secret_value = {
        "cohort_id": "de_2024_09_02",
        "host": "rds.com",
        "username": "alpha",
        "password": "beta",
        "database": "gamma",
        "port": 5432,
    }
    
    # Create mock response
    mock_response = {
        'SecretString': json.dumps(secret_value)
    }
    
    # Create mock Secrets Manager client
    mock_client = Mock()
    mock_client.get_secret_value = Mock(return_value=mock_response)
    
    # Patch boto3.client to return our mock client
    with patch('boto3.client', return_value=mock_client):
        result = get_secret('source_rds_credentials')
        
        # Verify the result
        assert json.loads(result) == secret_value
        
        # Verify the mock was called correctly
        mock_client.get_secret_value.assert_called_once_with(
            SecretId='source_rds_credentials'
        )

def test_get_secret_miss_secret():
    # Create mock error response
    error_response = {
        'Error': {
            'Code': 'ResourceNotFoundException',
            'Message': 'Secrets Manager can''t find the specified secret.'
        }
    }
    
    # Create mock client that raises an exception
    mock_client = Mock()
    mock_client.get_secret_value = Mock(
        side_effect=ClientError(error_response, 'GetSecretValue')
    )
    
    # Patch boto3.client to return our mock client
    with patch('boto3.client', return_value=mock_client):
        result = get_secret('nonexistent')
        
        # Verify the result
        assert result is None
        
        # Verify the mock was called correctly
        mock_client.get_secret_value.assert_called_once_with(
            SecretId='nonexistent'
        )