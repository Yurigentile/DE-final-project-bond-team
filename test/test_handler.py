from src.extract_lambda.handler import lambda_handler
from unittest.mock import patch
from src.s3_helpers import retrieve_list_of_s3_files


def test_lambda_handler_upload_to_s3():
    # Mock the boto3 client's put_object method
    with patch("src.s3_save_utilities.s3_client.put_object") as mock_put_object:
        # Call the function with a mock event
        lambda_handler(
            {
                "task": "upload_to_s3",
                "data": {"example": "data"},
                "bucket": "my-bucket",
                "key": "path/to/file.json",
            },
            None,
        )

        # Simply assert that put_object was called
        mock_put_object.assert_called()


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
