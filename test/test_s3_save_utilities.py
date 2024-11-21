import boto3
import unittest
from unittest.mock import patch, Mock
import json
from extract_lambda.src.s3_save_utilities import s3_save_as_json, s3_save_as_csv
from moto import mock_aws


class TestS3Save(unittest.TestCase):
    @patch("builtins.print")
    @mock_aws
    def test_s3_save(self, mock_print):
        # Setup mock values to be passed from the lambda
        bucket = "testbucket"
        key = "test.json"
        data = {"example": "data"}

        # Create a mock S3 client
        s3_client = boto3.client("s3", region_name="us-east-1")

        # Create the bucket in the mock S3 environment
        s3_client.create_bucket(Bucket=bucket)

        # Call the s3_save function to save the data
        s3_save_as_json(data, bucket, key)

        # Verify that the object was saved correctly
        response = s3_client.get_object(Bucket=bucket, Key=key)
        saved_data = json.loads(response["Body"].read().decode("utf-8"))

        # Assertions to verify the saved data and content type
        self.assertEqual(saved_data, data)
        self.assertEqual(response["ContentType"], "application/json")
        mock_print.assert_called_with(f"Saved to {bucket}/{key}")
    
    @patch("builtins.print")
    @patch("boto3.client")
    def test_s3_save_error_handling(self, mock_boto_client, mock_print):
        # Setup the mock S3 client and simulate an error on put_object
        bucket = "testbucket"
        key = "test.json"
        data = {"example": "data"}

        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3
        mock_s3.put_object.side_effect = Exception("test error")

        # Call the function and assert that print was called with the error message
        s3_save_as_json(data, bucket, key)

        # Check that the error message was printed
        mock_print.assert_called_with("Error: test error")


class TestS3SaveAsCSV(unittest.TestCase):
    @patch("builtins.open")
    @patch("os.remove")
    @mock_aws
    def test_s3_save_as_csv(self, mock_remove, mock_open):
        # Create a mock S3 client
        s3_client = boto3.client("s3", region_name="eu-west-2")

        # Create the bucket in the mock S3 environment
        bucket = "test-bucket"
        s3_client.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

        # Define test data
        key = "test-folder/test.csv"
        headers = ["id", "name", "age"]
        data = [[1, "Yuri", 25], [2, "Bob", 30]]

        # Call function to test
        s3_save_as_csv(data, headers, bucket, key)

        # Assert open was called twice (once for write, once for read)
        self.assertEqual(mock_open.call_count, 2)

        # Verify S3 upload
        response = s3_client.get_object(Bucket=bucket, Key=key)
        saved_data = response["Body"].read().decode("utf-8")
        expected_csv = "id,name,age\n1,Yuri,25\n2,Bob,30\n"
        self.assertEqual(saved_data, expected_csv)
        self.assertEqual(response["ContentType"], "text/csv")

        # Verify temp file cleanup
        mock_remove.assert_called_once()


if __name__ == "__main__":
    unittest.main()
