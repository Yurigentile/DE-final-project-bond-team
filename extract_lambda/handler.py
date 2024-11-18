from datetime import datetime
import re
import logging

import os
if os.environ.get("AWS_EXECUTION_ENV") is not None:
    from src.s3_save_utilities import s3_save_as_json
    from src.s3_helpers import retrieve_list_of_s3_files
    from src.secrets_manager import get_secret
    from src.db_connection import create_conn
    from src.db_query import get_latest_data
    # For use in lambda function
else:
    # For local use
    from extract_lambda.src.s3_save_utilities import s3_save_as_json
    from extract_lambda.src.s3_helpers import retrieve_list_of_s3_files
    from extract_lambda.src.secrets_manager import get_secret
    from extract_lambda.src.db_connection import create_conn
    from extract_lambda.src.db_query import get_latest_data
    

def lambda_handler(event, context):
    """
    AWS Lambda Handler to extract latest data from Postgres database and upload to AWS S3 bucket.

    
    Events format:

        {
            "secret" = "aws_secretsmanager_secret_name,"
            "bucket" = "aws_s3_bucket_name"
        }

    The S3 bucket folders structure looks like this:

    bucket-name
        2024-11-15 23:00:00
            design.json
            sales_order.json
            staff.json
            currency.json
            counterparty.json
            address.json
            department.json
            purchase_order.json
            payment_type.json
            payment.json
            transaction.json
        2024-11-15 23:30:00
            design.json
            sales_order.json
            staff.json
            currency.json
            counterparty.json
            address.json
            department.json
            purchase_order.json
            payment_type.json
            payment.json
            transaction.json

    Each folder represents timestamp of the lambda function run.
    Each JSON object in bucket represents data delta since the last sync time.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    
    secret = event.get("secret")
    bucket = event.get("bucket")

    logger.info("Passed event: secret=%s, bucket=%s", secret, bucket)

    objects_list = retrieve_list_of_s3_files(bucket)
    
    if len(objects_list) == 0:
        last_sync_timestamp = '2000-01-01 00:00:00'
    else:
        sorted_object_list = sorted(objects_list)

        last_object_name = sorted_object_list[-1]

        last_sync_timestamp = re.match(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})/", last_object_name).group(1)

    database_credentials_string = get_secret(secret)

    conn = create_conn(database_credentials_string)

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

    latest_data = get_latest_data(conn, tables, last_sync_timestamp)

    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for table, rows in latest_data.items():
        s3_save_as_json(rows, bucket, f"{current_timestamp}/{table}.json")