from lambda_extract.src.s3_helpers import (
    create_object_with_datetime_key as cod,
    retrieve_list_of_s3_files,
)
import re
import unittest
from unittest.mock import patch, Mock
import boto3
from botocore.exceptions import NoCredentialsError


def test_create_object_with_datetime_key_is_valid_path():
    # Invoke the function
    test_function = cod("extract")

    # Use regex to create a pattern for folder name, iso datetime format and json extension
    match = r"^extract/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}\.json$"

    # Assert to verify output
    assert re.match(match, test_function) is not None


def test_create_object_with_datetime_key_for_uniqueness():
    # Invoke the function
    test_function_with_key1 = cod("extract")
    # Invoke the function again
    test_function_with_key2 = cod("extract")

    # Assert the returned keys are different
    assert test_function_with_key1 != test_function_with_key2


def test_create_object_with_datetime_key_aws_compatibility():
    # Invoke the function
    test_function = cod("extract")

    # Assert correct separator aws
    assert "/" in test_function
    # Assert non compatible separator doesn't exist
    assert "\\" not in test_function


class TestS3Functions(unittest.TestCase):
    @patch("boto3.client")
    def setUp(self, mock_boto_client):
        # Mock S3 client
        self.mock_s3 = Mock()
        mock_boto_client.return_value = self.mock_s3

        # Mock bucket data
        def mock_list_objects_v2(Bucket):
            if Bucket == "test-bucket":
                return {
                    "Contents": [
                        {"Key": "fake_file1.json"},
                        {"Key": "fake_file2.json"},
                        {"Key": "fake_file3.json"},
                    ]
                }
            return {}

        self.mock_s3.list_objects_v2.side_effect = mock_list_objects_v2

    @patch("boto3.client")
    def test_retrieve_list_of_s3_files_when_bucket_has_files(self, mock_boto_client):
        mock_boto_client.return_value = self.mock_s3

        bucket = "test-bucket"
        result = retrieve_list_of_s3_files(bucket)
        self.assertEqual(
            result, ["fake_file1.json", "fake_file2.json", "fake_file3.json"]
        )

    @patch("boto3.client")
    def test_retrieve_list_of_s3_files_bucket_empty(self, mock_boto_client):
        mock_boto_client.return_value = self.mock_s3

        bucket = "empty-bucket"
        result = retrieve_list_of_s3_files(bucket)
        self.assertEqual(result, [])

    @patch("boto3.client")
    def test_retrieve_list_of_s3_files_bucket_no_credentials(self, mock_boto_client):
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        # Simulate NoCredentialsError
        mock_s3.list_objects_v2.side_effect = NoCredentialsError

        with self.assertRaises(NoCredentialsError):
            retrieve_list_of_s3_files("test-bucket")


if __name__ == "__main__":
    unittest.main()
