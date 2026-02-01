import json
import boto3
import logging
from botocore.exceptions import ClientError
import pandas as pd
from pg8000.native import Connection

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret(name):
    """Gets a secret from AWS Secret Manager.

    Finds the given secret name in the Secret Manager and returns the
    value.

    Args:
      name: secret name

    Returns:
      String value of the secret or an informative error message.

    """
    client = boto3.client("secretsmanager")
    try:
        response = client.get_secret_value(SecretId=name)
        secret_value = response["SecretString"]
        return secret_value
    except ClientError as e:
        print(f">>> Secret {name} was not found")
        return None


def create_conn(sm_params):
    """
    Returns pg8000 database connection

    Parameters:
        sm_params (json): JSON object containing the database credentials.

    Returns:
        pg8000 connection object

    Raises:
        Exception: Any exception raised by pg8000 will be printed

    Side Effects:
        Outputs 'Connected to database' message upon successful connection, or error upon exception

    Example usage with get_secret util function:
    >>> secrets = get_secret('totes-database')
    >>> conn = create_conn(secrets)
    """
    try:
        db_params = json.loads(sm_params)
        conn = Connection(
            database=db_params["database"],
            user=db_params["user"],
            password=db_params["password"],
            host=db_params["host"],
            port=db_params["port"],
            timeout=10,
        )
        print(f"Connected to database {db_params['database']}")
        return conn

    except Exception as e:
        print(f" Something went wrong: {e}")


def close_conn(conn):
    """
    Closes a database connection

    Parameters:
        conn (pg8000 connection object): a pg8000 connection to a database

    Returns:
        Nothing
    """
    conn.close()


def load_data_into_warehouse(dataframes, conn, schema="public"):
    """
    Loads DataFrames into a data warehouse (e.g., PostgreSQL) using pg8000.

    Parameters:
        dataframes (dict): A dictionary where each key is a table name and the value is a DataFrame.
        conn (pg8000.Connection): The database connection object.
        schema (str): The schema name in the data warehouse. Defaults to 'public'.

    Example:
        >>> load_data_into_warehouse(dataframes, conn)
    """

    ordered_tables_with_primary_keys = {
        "dim_date": "date_id",
        "dim_staff": "staff_id",
        "dim_location": "location_id",
        "dim_design": "design_id",
        "dim_currency": "currency_id",
        "dim_counterparty": "counterparty_id",
        "fact_sales_order": "sales_record_id",
    }

    for table, primary_key in ordered_tables_with_primary_keys.items():
        df = dataframes[table]

        try:
            logger.info(f"Upserting table: {table} (Rows: {len(df)})")

            cols = ", ".join(f'"{col}"' for col in df.columns)
            placeholders = ", ".join(f":{col}" for col in df.columns)
            updates = ", ".join(f'"{col}" = EXCLUDED."{col}"' for col in df.columns)
            query = f"""
                INSERT INTO {schema}.{table} ({cols}) 
                VALUES ({placeholders})
                ON CONFLICT ("{primary_key}") DO UPDATE
                SET {updates};
            """

            for row in df.to_dict(orient="records"):
                conn.run(query, **row)

            logger.info(f"Successfully upserted table: {table}")

        except Exception as load_error:
            logger.error(f"Failed to upsert table {table}: {load_error}")
