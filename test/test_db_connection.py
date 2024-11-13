from src.db_connection import create_conn
from src.secrets_manager import get_secret
import unittest
from unittest.mock import patch, MagicMock
from moto import mock_aws
import boto3
import pytest
import json
from botocore.exceptions import ClientError

@mock_aws
def test_get_secret_connection():
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
  secret_value_from_func = get_secret(secret_name)
  print(create_conn(secret_value_from_func))
  #print(json.loads(get_secret(secret_name)))
  #assert json.loads(get_secret(secret_name)) == secret_value