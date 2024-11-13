from pg8000.native import Connection
from src.secrets_manager import get_secret
import json

# Create your create_conn function to return a database connection object
def create_conn(sm_params):
    db_params = json.loads(sm_params)
    print(sm_params)
    print(db_params)
    # try:
    #     conn = Connection(
    #         cohort_id = db_params['cohort_id'],
    #         database=db_params['database'],
    #         user=db_params['user'],
    #         password=db_params['password'],
    #         host = db_params['host'],
    #         port = db_params['port']
    #     )
    #     return conn

    # except Exception as e:
    #     print (f' Something went wrong: {e}')
    