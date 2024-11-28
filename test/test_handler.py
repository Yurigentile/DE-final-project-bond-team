from lambda_extract.handler import lambda_handler
from unittest.mock import patch, Mock
from lambda_extract.src.s3_helpers import retrieve_list_of_s3_files
import boto3
from datetime import datetime
from decimal import Decimal
from moto import mock_aws


@mock_aws
def test_lambda_handler_run():
    secret = "test-secret"
    bucket = "test-data"
    region = "eu-west-2"

    boto3.client("s3", region_name=region).create_bucket(
        Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region}
    )

    boto3.client("secretsmanager", region_name=region).create_secret(
        Name=secret,
        SecretString='{"user": "test_user", "password": "test", "host": "localhost", "database": "test_database", "port": 5432}',
    )

    event = {
        "secret": secret,
        "bucket": bucket,
    }

    lambda_handler(event, None)

    object_list = boto3.client("s3", region_name=region).list_objects_v2(Bucket=bucket)
    # Unfortunately S3 doesn't allow to list objects by suffix, hence own filtering is required
    matched_object = [
        obj
        for obj in object_list["Contents"]
        if obj["Key"].endswith("sales_order.json")
    ][0]
    object_key = matched_object["Key"]

    object = boto3.client("s3", region_name=region).get_object(
        Bucket=bucket, Key=object_key
    )
    content = object["Body"].read().decode("utf-8")

    assert content == (
        '[{"sales_order_id": 11165, "created_at": "2024-11-14T10:19:09.990000", '
        '"last_updated": "2024-11-14T10:19:09.990000", "design_id": 472, "staff_id": '
        '18, "counterparty_id": 19, "units_sold": 12145, "unit_price": 3.83, '
        '"currency_id": 3, "agreed_delivery_date": "2024-11-15", '
        '"agreed_payment_date": "2024-11-15", "agreed_delivery_location_id": 26}, '
        '{"sales_order_id": 11166, "created_at": "2024-11-14T11:36:10.342000", '
        '"last_updated": "2024-11-14T11:36:10.342000", "design_id": 473, "staff_id": '
        '14, "counterparty_id": 20, "units_sold": 75609, "unit_price": 3.52, '
        '"currency_id": 3, "agreed_delivery_date": "2024-11-15", '
        '"agreed_payment_date": "2024-11-20", "agreed_delivery_location_id": 7}]'
    )

    matched_object = [
        obj
        for obj in object_list["Contents"]
        if obj["Key"].endswith("transaction.json")
    ][0]
    object_key = matched_object["Key"]

    object = boto3.client("s3", region_name=region).get_object(
        Bucket=bucket, Key=object_key
    )
    content = object["Body"].read().decode("utf-8")

    assert content == "[]"

    # TODO: Test second run
    # lambda_handler(event, None)


def xtest_lambda_handler_upload_to_s3():
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
        "ResponseMetadata": {"HTTPStatusCode": 200}
    }

    # Patch boto3.client to return our mock
    with patch("boto3.client", return_value=mock_s3_client):
        response = lambda_handler(event, None)

        # Verify put_object was called with correct arguments
        mock_s3_client.put_object.assert_called_once()
        call_args = mock_s3_client.put_object.call_args[1]
        assert call_args["Bucket"] == "my-bucket"
        assert call_args["Key"] == "path/to/file.json"
        assert isinstance(call_args["Body"], str)


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
