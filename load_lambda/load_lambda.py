import logging
import os

if os.environ.get("AWS_EXECUTION_ENV") is not None:
    # For use in lambda function
    # from src.secrets_manager import get_secret
    # from src.db_connection import create_conn
    from src.load_parquet_data import read_parquet_data_to_dataframe

else:
    # For local use
    # from load_lambda.src.secrets_manager import get_secret
    # from load_lambda.src.db_connection import create_conn
    from load_lambda.src.load_parquet_data import read_parquet_data_to_dataframe


def lambda_handler(event, context):
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        secret = event.get("secret")
        bucket = event.get("bucket")

        logger.info("Passed event: secret=%s, bucket=%s", secret, bucket)

        # retrieve db credentials from AWS Secrets Manager 
        # database_credentials_string = get_secret(secret)

        # create db connection
        # conn = create_conn(database_credentials_string)

        # retrieve most recent set of parquet files from bucket and return as dataframes
        data = read_parquet_data_to_dataframe(bucket)

        # PSQL Load function goes here
        ##################################

    except Exception as e:
        print(f"Error: {e}")
