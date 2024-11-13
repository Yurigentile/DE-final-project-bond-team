from src.s3_helpers import create_object_with_datetime_key as cod, retrieve_list_of_s3_files
import re
import unittest
from unittest.mock import patch
import boto3
from moto import mock_aws
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


@mock_aws
class TestS3Functions(unittest.TestCase):

    def setUp(self):
        # Create mock client and buckets
        region = 'eu-west-2'
        self.s3 = boto3.client('s3')
        self.s3.create_bucket(Bucket='test-bucket', CreateBucketConfiguration={"LocationConstraint": region})
        self.s3.create_bucket(Bucket='empty-bucket', CreateBucketConfiguration={"LocationConstraint": region})

        # Fill the test-bucket
        self.s3.put_object(Bucket='test-bucket', Key='fake_file1.json', Body='content')
        self.s3.put_object(Bucket='test-bucket', Key='fake_file2.json', Body='content')
        self.s3.put_object(Bucket='test-bucket', Key='fake_file3.json', Body='content')

    def test_retrieve_list_of_s3_files_when_bucket_has_files(self):
        bucket = 'test-bucket'
        result = retrieve_list_of_s3_files(bucket)
        
        # Assert to verify all files were retrieved
        self.assertEqual(result, ['fake_file1.json', 'fake_file2.json', 'fake_file3.json'])

    def test_retrieve_list_of_s3_files_bucket_empty(self):
        bucket = 'empty-bucket'
        result = retrieve_list_of_s3_files(bucket)
        
        # Assert to verify an empty list is returned
        self.assertEqual(result, [])

    @patch('boto3.client')
    def test_retrieve_list_of_s3_files_bucket_no_credentials(self, mock_boto):
        # Create mock NoCredentialsError
        mock_s3 = mock_boto.return_value
        mock_s3.list_objects_v2.side_effect = NoCredentialsError

        # Assert error is raised
        with self.assertRaises(NoCredentialsError):
            retrieve_list_of_s3_files('test-bucket')

if __name__ == '__main__':
    unittest.main()