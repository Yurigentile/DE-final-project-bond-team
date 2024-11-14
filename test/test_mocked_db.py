from db.mocked_db import function_to_tets
from unittest import mock
import pandas as pd


@mock.patch('db.mocked_db.sqlite3')
@mock.patch('db.mocked_db.pd.read_sql_query')
def test_sql_query(read_sql_query_mock, sqlite_mock):
    read_sql_query_mock.return_value = pd.DataFrame({'design_id': ['design_id 1', 'cjodso'],
                                                     'last_updated': ['last_updated 1', 'ckd'],
                                                     'design_name': ['design_name 1', 'doksod']})
    assert function_to_tets().to_dict(orient='list') == {'design_id': ['design_id 1', 'cjodso'],
                                                         'last_updated': ['last_updated 1', 'ckd'],
                                                         'design_name': ['design_name 1', 'doksod']}