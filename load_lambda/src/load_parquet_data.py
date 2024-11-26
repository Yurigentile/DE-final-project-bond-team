import boto3
import re
import awswrangler as wr
from datetime import datetime


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


def read_parquet_data_to_dataframe(bucket):
    """
    Retrives data from objects in s3 bucket and reads them to DataFrame

    This function retrieves and returns the dictionary with all last updated objects
    stored in the specified Amazon S3 bucket in DataFrame format.

    Parameters:
        bucket_name (str): The name of the S3 bucket to retrieve file names from.
        tables (str): List of table names which are to be added to data warehouse

    Returns:
        A dictionary, where each key represents table and value represents a parquet file converted to DataFrame.

    Example:
        >>> read_parquet_data_to_dataframe('my-bucket')
            {'dim_design':    design_id design_name file_location                  file_name
                0        477      Bronze          /lib  bronze-20230409-joj9.json,
            'dim_date':       date_id  year  month  day  day_of_week   day_name month_name  quarter
                0  2024-11-19  2024     11   19            1    Tuesday   November        4}

    Raises:
        Exception: Any exception raised will be caught, printed, and re-raised.
    """

    tables = [
        'fact_sales_order',
        'dim_staff',
        'dim_location',
        'dim_design',
        'dim_date',
        'dim_currency',
        'dim_counterparty'
    ]
    try:
        object_list = retrive_list_of_files(bucket)
        result = {}
        sorted_files_list = sorted(object_list)
        last_object_list = sorted_files_list[-1]
        last_sync_timestamp = re.match(
            r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2})/", last_object_list
        ).group(1)
        for table in tables:
            try:
                result[table] = wr.s3.read_parquet(path=[f"s3://{bucket}/{last_sync_timestamp}/{table}.parquet"])
            except:
                pass

        return result
    except Exception as e:
        print(f"Error: {e}")
