import boto3
from botocore.exceptions import ClientError




def get_secret(name):
    """Gets a secret from AWS Secret Manager.

    Finds the given secret name in the Secret Manager and returns the
    value.

    Args:
      name: secret name

    Returns:
      String value of the secret or an informative error message.

    """
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=name)
        secret_value = response["SecretString"]
        return secret_value
    except ClientError as e:
        print(f">>> Secret {name} was not found")
        return None
