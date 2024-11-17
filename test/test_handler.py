from src.extract_lambda.handler import lambda_handler
from unittest.mock import patch, Mock
from src.s3_helpers import retrieve_list_of_s3_files
import boto3
from moto import mock_aws
import pprint
import logging

@mock_aws(config={
    "core": {
        "mock_credentials": False,
        "passthrough": {
            "services": ["secretsmanager"]
        }
    }
})
def test_lambda_handler_run():
    logger = logging.getLogger()

    bucket = "test-data"
    region = 'eu-west-2'

    boto3.client("s3").create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region})

    event = {
        "secret": "totes-database",
        "bucket": bucket,
    }

    # First run
    lambda_handler(event, None)

    object_list = boto3.client("s3").list_objects_v2(Bucket=bucket)
    logger.debug(pprint.pformat(object_list))

    last_object_key = object_list['Contents'][-1]['Key']

    object = boto3.client("s3").get_object(Bucket=bucket, Key=last_object_key)
    content = object['Body'].read().decode('utf-8')

    logger.debug(content)

    # Second run
    # lambda_handler(event, None)

def test_lambda_handler_upload_to_s3():
    """Test successful S3 upload scenario"""
    event = {
        "task": "upload_to_s3",
        "data": {"example": "data"},
        "bucket": "my-bucket",
        "key": "path/to/file.json",
    }
    
    # Create a mock for the S3 client
    mock_s3_client = Mock()
    mock_s3_client.put_object.return_value = {
        'ResponseMetadata': {'HTTPStatusCode': 200}
    }
    
    # Patch boto3.client to return our mock
    with patch('boto3.client', return_value=mock_s3_client):
        response = lambda_handler(event, None)
        
        # Verify put_object was called with correct arguments
        mock_s3_client.put_object.assert_called_once()
        call_args = mock_s3_client.put_object.call_args[1]
        assert call_args['Bucket'] == 'my-bucket'
        assert call_args['Key'] == 'path/to/file.json'
        assert isinstance(call_args['Body'], str)


def test_retrieve_files():
    with patch("boto3.client") as mock_s3_client:
        mock_s3_instance = mock_s3_client.return_value
        mock_s3_instance.list_objects_v2.return_value = {
            "Contents": [{"Key": "file1.json"}, {"Key": "file2.json"}]
        }

        # Call the function that interacts with S3
        retrieve_list_of_s3_files("my-bucket")

        # Assert that list_objects_v2 was called once with the correct parameters
        mock_s3_instance.list_objects_v2.assert_called_once_with(Bucket="my-bucket")


def test_lambda_handler_unknown_task(caplog):
    # Call with an invalid task
    lambda_handler({"task": "invalid_task"}, None)

    # Assert that the log contains the 'Unknown task' message
    assert "Unknown task" in caplog.text
