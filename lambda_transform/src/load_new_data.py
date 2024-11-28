import json
import boto3
import re
from datetime import datetime
from pprint import pprint


def retrive_list_of_files(bucket):
    """
    List all file names in an Amazon S3 bucket.

    This function retrieves and returns the names of all objects stored in the specified
    Amazon S3 bucket. If the bucket is empty, an empty list is returned.

    Parameters:
        bucket_name (str): The name of the S3 bucket to retrieve file names from.

    Returns:
        list: A list of file names (str) in the bucket. Returns an empty list if the bucket
              contains no files.

    Example:
        >>> retrieve_list_of_s3_files('my-bucket')
        ["2024-11-19 21:05:55/staff.json", "2024-11-19 21:05:55/transaction.json"]

    Raises:
        botocore.exceptions.NoCredentialsError: If AWS credentials are not available.
        botocore.exceptions.ClientError: For other client errors, such as permissions issues.
    """

    s3_client = boto3.client("s3")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    response = s3_client.list_objects_v2(Bucket=bucket,Prefix=timestamp)

    if "Contents" in response:
        return [obj["Key"] for obj in response["Contents"]]
    return []


def load_new_data(bucket, tables):
    """
    Retrives data from objects in s3 bucket.

    This function retrieves and returns the dictionary with all last updated objects
    stored in the specified Amazon S3 bucket.

    Parameters:
        bucket_name (str): The name of the S3 bucket to retrieve file names from.
        tables (str): List of table names to query from the db

    Returns:
        A dictionary, where each key represents table and value represents list of dictionaries.
        The nested list represents queried database rows.

    Example:
        >>> load_new_data('my-bucket')
        {'address': [],
            'sales_order': [{'agreed_delivery_date': '2024-11-24',
                            'agreed_delivery_location_id': 8,
                            'agreed_payment_date': '2024-11-19',
                            'counterparty_id': 12,
                            'created_at': '2024-11-19T14:26:09.927000',
                            'currency_id': 3,
                            'design_id': 140,
                            'last_updated': '2024-11-19T14:26:09.927000',
                            'sales_order_id': 11235,
                            'staff_id': 5,
                            'unit_price': 3.96,
                            'units_sold': 77240}],
            'staff': [],
            'transaction': [{'created_at': '2024-11-19T14:26:09.927000',
                            'last_updated': '2024-11-19T14:26:09.927000',
                            'purchase_order_id': None,
                            'sales_order_id': 11235,
                            'transaction_id': 15903,
                            'transaction_type': 'SALE'}]}

    Raises:
        Exception: Any exception raised by boto3's put_object function will be caught, printed, and re-raised.
    """

    s3_client = boto3.client("s3")
    tables = [
        "design",
        "sales_order",
        "staff",
        "currency",
        "counterparty",
        "address",
        "department",
        "purchase_order",
        "payment_type",
        "payment",
        "transaction",
    ]
    try:
        object_list = retrive_list_of_files(bucket)
        result = {}
        sorted_files_list = sorted(object_list)
        last_object_list = sorted_files_list[-1]
        last_sync_timestamp = re.match(
            r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})/", last_object_list
        ).group(1)
        for table in tables:
            response = s3_client.get_object(
                Bucket=bucket, Key=f"{last_sync_timestamp}/{table}.json"
            )
            data = json.loads(response["Body"].read().decode("utf-8"))
            result[table] = data
        # pprint(result)
        return result
    except Exception as e:
        print(f"Error: {e}")
