import logging
import os

if os.environ.get("AWS_EXECUTION_ENV") is not None:
    # For use in lambda function
    # from src.warehouse_load_functions import get_secret, alchemy_db_connection, alchemy_close_connection, load_data_into_warehouse
    from src.load_parquet_data import read_parquet_data_to_dataframe

else:
    # For local use
    # from load_lambda.src.warehouse_load_functions import get_secret, alchemy_db_connection, alchemy_close_connection, load_data_into_warehouse
    from load_lambda.src.load_parquet_data import read_parquet_data_to_dataframe


def lambda_handler(event, context):
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)   

        secret = event.get("secret")
        bucket = event.get("bucket")

        logger.info("Passed event: secret=%s, bucket=%s", secret, bucket)

        # retrieve most recent set of parquet files from bucket and return as dataframes
        data = read_parquet_data_to_dataframe(bucket)

        # Retrieve secret, create db connection and load dataframes into warehouse
        # load_data_into_warehouse(data, secret)

    except Exception as e:
        print(f"Error: {e}")