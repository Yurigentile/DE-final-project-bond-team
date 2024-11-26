#new secrets manager
#connect to db
#load dataframes as sql into warehouse
import json
import boto3
import logging
from botocore.exceptions import ClientError
from sqlalchemy import create_engine

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret(name):
    """Gets a secret from AWS Secret Manager with CloudWatch logging.
    
    Finds the given secret name in the Secret Manager and returns the
    value as a dictionary, logging key events and potential errors.
    
    Args:
      name: secret name
    
    Returns:
      Dictionary containing the secret or None if not found.
    """
    secretsmanager_client = boto3.client("secretsmanager", region_name = 'eu-west-2')
    
    try:
        logger.info(f"Retrieving: {name}")
        
        response = secretsmanager_client.get_secret_value(SecretId=name)
        secret_string = response.get("SecretString")
        
        if secret_string is None:
            logger.error(f"Secret '{name}' has no string value.")
            return None
        
        secret_value = json.loads(secret_string)
        logger.info(f"Secret retrieved successfully: {name}")
        return secret_value
    
    except json.JSONDecodeError as e:
        logger.error(f"Secret '{name}' could not be parsed as JSON: {str(e)}")
        return None
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        logger.error(f"Error retrieving '{name}': "
                     f"Code: {error_code}, "
                     f"Message: {error_message}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error retrieving '{name}': {str(e)}")
        return None
    
def alchemy_db_connection(name):
    """
    Establishes a connection to the PostgreSQL database using SQLAlchemy.

    Parameters:
        name (str): The name of the secret to retrieve the database credentials.

    Returns:
        A SQLAlchemy engine object.

    Raises:
        Exception: If database connection fails.
    """
    try:
        logger.info(f"Attempting to retrieve credentials for secret: {name}")

        db_params_json = get_secret(name)

        if not db_params_json:
            logger.error(f"Failed to retrieve credentials for secret: {name}")
            raise ValueError(f"Could not retrieve credentials for {name}")

        db_params = json.loads(db_params_json)

        masked_conn_str = f"postgresql+psycopg2://{db_params['username']}:****@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
        logger.info(f"Attempting to create connection: {masked_conn_str}")

        conn_str = f"postgresql+psycopg2://{db_params['username']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"

        engine = create_engine(conn_str)

        with engine.connect() as connection:
            logger.info(f"Successfully established database connection to {db_params['host']}:{db_params['port']}/{db_params['dbname']}")

        return engine

    except ValueError as ve:
        logger.error(f"Validation error in database connection: {ve}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to database: {e}", exc_info=True)
        raise

def alchemy_close_connection(engine):
    """
    Properly closes the database engine and releases resources.
    
    Parameters:
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine to close.
    """
    try:
        if engine:
            engine.dispose()
            logger.info("Database connection engine closed")
    except Exception as e:
        logger.error(f"Error closing engine connection: {e}")

def load_data_into_warehouse(dataframes, db_params, schema='public'):
    """
    Loads DataFrames into a data warehouse (e.g., PostgreSQL).

    Parameters:
        dataframes (dict): A dictionary where each key is a table name and the value is a DataFrame.
        db_params (dict): A dictionary containing the database connection parameters.
        schema (str): The schema name in the data warehouse. Defaults to 'public'.

    Example:
        >>> load_data_into_warehouse(dataframes, db_params)
    """
    engine = alchemy_db_connection(db_params)

    for table, df in dataframes.items():
        try:
            logger.info(f"Loading table: {table} (Rows: {len(df)})")
            
            df.to_sql(
                name=table,
                con=engine,
                schema=schema,
                if_exists='append',
                index=False
            )
            
            logger.info(f"Successfully loaded table: {table}")
        
        except Exception as load_error:
            logger.error(f"Failed to load table {table}: {load_error}") 