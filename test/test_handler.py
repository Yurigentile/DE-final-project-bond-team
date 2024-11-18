from extract_lambda.handler import lambda_handler
from unittest.mock import patch, Mock
from extract_lambda.src.s3_helpers import retrieve_list_of_s3_files


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
