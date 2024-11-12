import unittest
from unittest.mock import patch
import boto3
from moto import mock_aws
import json
from src.utilities import s3_save


@mock_aws
class TestS3Save(unittest.TestCase):
    
    @patch("builtins.print")
    def test_s3_save(self, mock_print):
        # Setup mock values to be passed from the lambda
        bucket = "testbucket"
        key = "test.json"
        data = {"example": "data"}
        region = "eu-west-2"

        # Initialise the client for mock
        s3_client = boto3.client("s3", region_name=region)

        # Create the bucket for testing purposes in the mock S3 environment
        s3_client.create_bucket(
            Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region}
        )

        # Call the s3_save function to save the data
        s3_save(data, bucket, key)

        # Confirm the object exists in the bucket with the correct content
        response = s3_client.get_object(Bucket=bucket, Key=key)
        saved_data = json.loads(response["Body"].read().decode("utf-8"))

        # Assertions to verify the saved data and content type
        self.assertEqual(saved_data, data)
        self.assertEqual(response["ContentType"], "application/json")
        mock_print.assert_called_with(f"Saved to {bucket}/{key}")
        
    def test_s3_save_error_handling(self):
        # Setup mock values to be passed from the lambda
        bucket = "testbucket"
        key = "test.json"
        data = {"example": "data"}
        region = "eu-west-2"

        # Initialise the client for mock
        s3_client = boto3.client("s3", region_name=region)

        # Create the bucket for testing purposes in the mock S3 environment
        s3_client.create_bucket(
            Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region}
        )

        # Patch the boto3.client and mock the s3 service
        with patch("boto3.client") as mock_boto_client:
            mock_s3 = mock_boto_client.return_value
            # Create a custom error for put_object
            mock_s3.put_object.side_effect = Exception("test error")

            # Assert for verifying error was raised
            with self.assertRaises(Exception) as detail:
                # Call the function
                s3_save(data, bucket, key)

                # Assert for verifying error message is output
                self.assertEqual(str(detail.exception))

if __name__ == "__main__":
    unittest.main()
