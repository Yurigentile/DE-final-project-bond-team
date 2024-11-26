from pg8000.native import Connection
import json


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
