from pg8000.native import identifier

def get_latest_data(conn, tables, sync_timestamp):

    """
    Retrieves rows from specified tables in a PostgreSQL database where the `last_updated`
    column is greater than a given sync timestamp.

    This function executes SELECT query on each table provided in the `tables` list, filtering
    the results by the `last_updated` timestamp.

    Parameters:
        conn: An active connection to the PostgreSQL database
        tables: A list of table names (strings) to query from the database
        sync_timestamp: Last sync timestamp (string)

    Returns:
        A dictionary, where each key represents table and value represents list of dictionaries.
        The nested list represents queried database rows
    
        Example:
        {
            'table_name_1': [],
            'table_name_2': [
                {
                    'column_1': cell_1,
                    'column_2': cell_2
                },
                {

                    'colomn_1': cell_1,
                    'column_2': cell_2
                }
            ]
        }
    """
    result = {}
    try:
        for table in tables:
            rows = conn.run(f"SELECT * FROM {identifier(table)} WHERE last_updated > :sync_timestamp", sync_timestamp=sync_timestamp)
            columns = [col["name"] for col in conn.columns]
            result[table] = [dict(zip(columns, row)) for row in rows] 
        print(result)
        return result
    finally:
        conn.close()
