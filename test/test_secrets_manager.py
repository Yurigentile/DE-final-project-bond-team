from moto import mock_aws
import boto3
import pytest
import json
from botocore.exceptions import ClientError
from src.secrets_manager import get_secret

@mock_aws
def test_get_secret_find_secret():
  client = boto3.client('secretsmanager')

  secret_name = "source_rds_credentials"
  secret_value = {
    "cohort_id": "de_2024_09_02",
    "host": "rds.com",
    "username": "alpha",
    "password": "beta",
    "database": "gamma",
    "port": 5432
  }
  
  client.create_secret(Name=secret_name, SecretString=json.dumps(secret_value))

  assert json.loads(get_secret(secret_name)) == secret_value

@mock_aws
def test_get_secret_miss_secret():
  client = boto3.client('secretsmanager')

  secret_name = "source_rds_credentials"
  secret_value = {
    "cohort_id": "de_2024_09_02",
    "host": "rds.com",
    "username": "alpha",
    "password": "beta",
    "database": "gamma",
    "port": 5432
  }
  
  client.create_secret(Name=secret_name, SecretString=json.dumps(secret_value))

  assert get_secret("nonexistent") == None