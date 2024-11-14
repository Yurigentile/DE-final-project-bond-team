import sqlite3
import pandas as pd
from src.secrets_manager import get_secret
from src.db_connection import create_conn


def function_to_tets():
    df = None
    try:
        secrets = get_secret('totes-database')
        #db_connect = create_conn(secrets)
        db_connect = sqlite3.connect(secrets)
        db_cur = db_connect.cursor()
        db_cur.execute("""SELECT design_id, last_updated, design_name FROM design""")
        sql_result = pd.read_sql_query("""SELECT design_id, last_updated, design_name FROM design""", db_connect)
        df = pd.DataFrame(sql_result, columns=['design_id', 'last_updated', 'design_name'])
        print(f"The data from database is :\n {df}")
        db_cur.close()
        db_connect.close()
    except Exception as e:
        print(f"DB exception: {e}")

    return df