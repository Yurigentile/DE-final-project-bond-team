import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('secretsmanager')

def get_secret(name):
    try:
        response = client.get_secret_value(
            SecretId=name
        )
        secret_value = response['SecretString']
        return secret_value
    except ClientError as e:
        print(f">>> Secret {name} was not found")
        return None
