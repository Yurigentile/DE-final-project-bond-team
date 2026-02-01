import logging
import os

if os.environ.get("AWS_EXECUTION_ENV") is not None:
    # For use in lambda function
    from src.warehouse_load_functions_pg8000 import (
        get_secret,
        create_conn,
        close_conn,
        load_data_into_warehouse,
    )
    from src.load_parquet_data import read_parquet_data_to_dataframe

else:
    # For local use
    from lambda_load.src.warehouse_load_functions_pg8000 import (
        get_secret,
        create_conn,
        close_conn,
        load_data_into_warehouse,
    )
    from lambda_load.src.load_parquet_data import read_parquet_data_to_dataframe


def lambda_handler(event, context):
    """
    AWS Lambda Handler to load parquet data from S3 into the data warehouse.

    Events format:
        {
            "secret": "aws_secretsmanager_secret_name",
            "bucket": "aws_s3_bucket_name"
        }
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    conn = None
    try:
        secret = event.get("secret")
        bucket = event.get("bucket")

        logger.info("Passed event: secret=%s, bucket=%s", secret, bucket)

        # Retrieve most recent set of parquet files from bucket and return as dataframes
        data = read_parquet_data_to_dataframe(bucket)

        if not data:
            logger.warning("No data to load")
            return {"statusCode": 200, "body": "No data to load"}

        # Retrieve secret and create db connection
        secret_value = get_secret(secret)
        if not secret_value:
            logger.error("Failed to retrieve database credentials")
            return {"statusCode": 500, "body": "Failed to retrieve credentials"}

        conn = create_conn(secret_value)
        if not conn:
            logger.error("Failed to connect to database")
            return {"statusCode": 500, "body": "Failed to connect to database"}

        # Load dataframes into warehouse
        load_data_into_warehouse(data, conn)

        logger.info("Successfully loaded data into warehouse")
        return {"statusCode": 200, "body": "Data loaded successfully"}

    except Exception as e:
        logger.error(f"Error in lambda_handler: {e}")
        return {"statusCode": 500, "body": str(e)}

    finally:
        if conn:
            close_conn(conn)
