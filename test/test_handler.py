from extract_lambda.handler import lambda_handler
from unittest.mock import patch, Mock
from extract_lambda.src.s3_helpers import retrieve_list_of_s3_files
import boto3
from datetime import datetime
from decimal import Decimal


# @mock_aws(config={
#     "core": {
#         "mock_credentials": False,
#         "passthrough": {
#             "services": ["secretsmanager"]
#         }
#     }
# })
def xtest_lambda_handler_run():
    bucket = "test-data"
    region = "eu-west-2"

    boto3.client("s3").create_bucket(
        Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region}
    )

    event = {
        "secret": "totes-database",
        "bucket": bucket,
    }

    # TODO: Replace with test dataset when test database will appear
    dataset_stub = {
        "design": [
            {
                "design_id": 472,
                "created_at": datetime(2024, 11, 14, 9, 41, 9, 839000),
                "design_name": "Concrete",
                "file_location": "/usr/share",
                "file_name": "concrete-20241026-76vi.json",
                "last_updated": datetime(2024, 11, 14, 9, 41, 9, 839000),
            },
            {
                "design_id": 473,
                "created_at": datetime(2024, 11, 15, 14, 9, 9, 608000),
                "design_name": "Rubber",
                "file_location": "/Users",
                "file_name": "rubber-20240916-1hsu.json",
                "last_updated": datetime(2024, 11, 15, 14, 9, 9, 608000),
            },
        ],
        "sales_order": [
            {
                "sales_order_id": 11165,
                "created_at": datetime(2024, 11, 14, 10, 19, 9, 990000),
                "last_updated": datetime(2024, 11, 14, 10, 19, 9, 990000),
                "design_id": 69,
                "staff_id": 18,
                "counterparty_id": 19,
                "units_sold": 12145,
                "unit_price": Decimal("3.83"),
                "currency_id": 3,
                "agreed_delivery_date": "2024-11-15",
                "agreed_payment_date": "2024-11-15",
                "agreed_delivery_location_id": 26,
            },
            {
                "sales_order_id": 11166,
                "created_at": datetime(2024, 11, 14, 11, 36, 10, 342000),
                "last_updated": datetime(2024, 11, 14, 11, 36, 10, 342000),
                "design_id": 398,
                "staff_id": 14,
                "counterparty_id": 20,
                "units_sold": 75609,
                "unit_price": Decimal("3.52"),
                "currency_id": 3,
                "agreed_delivery_date": "2024-11-15",
                "agreed_payment_date": "2024-11-20",
                "agreed_delivery_location_id": 7,
            },
        ],
    }

    # Patch boto3.client to return our mock
    with patch("extract_lambda.handler.get_latest_data", return_value=dataset_stub):
        # First run
        lambda_handler(event, None)

    object_list = boto3.client("s3").list_objects_v2(Bucket=bucket)
    last_object_key = object_list["Contents"][-1]["Key"]

    object = boto3.client("s3").get_object(Bucket=bucket, Key=last_object_key)
    content = object["Body"].read().decode("utf-8")

    assert content == (
        '[{"sales_order_id": 11165, "created_at": "2024-11-14T10:19:09.990000", '
        '"last_updated": "2024-11-14T10:19:09.990000", "design_id": 69, "staff_id": '
        '18, "counterparty_id": 19, "units_sold": 12145, "unit_price": 3.83, '
        '"currency_id": 3, "agreed_delivery_date": "2024-11-15", '
        '"agreed_payment_date": "2024-11-15", "agreed_delivery_location_id": 26}, '
        '{"sales_order_id": 11166, "created_at": "2024-11-14T11:36:10.342000", '
        '"last_updated": "2024-11-14T11:36:10.342000", "design_id": 398, "staff_id": '
        '14, "counterparty_id": 20, "units_sold": 75609, "unit_price": 3.52, '
        '"currency_id": 3, "agreed_delivery_date": "2024-11-15", '
        '"agreed_payment_date": "2024-11-20", "agreed_delivery_location_id": 7}]'
    )

    # Second run
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


def xtest_retrieve_files():
    with patch("boto3.client") as mock_s3_client:
        mock_s3_instance = mock_s3_client.return_value
        mock_s3_instance.list_objects_v2.return_value = {
            "Contents": [{"Key": "file1.json"}, {"Key": "file2.json"}]
        }

        # Call the function that interacts with S3
        retrieve_list_of_s3_files("my-bucket")

        # Assert that list_objects_v2 was called once with the correct parameters
        mock_s3_instance.list_objects_v2.assert_called_once_with(Bucket="my-bucket")
