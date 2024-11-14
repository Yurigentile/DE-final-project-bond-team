from src.db_query import get_latest_data
from src.db_connection import create_conn
from src.secrets_manager import get_secret
from datetime import datetime, timedelta

def test_get_latest_data():
    secret = get_secret('totes-database')
    conn = create_conn(secret)
    tables = [
        "design",
        "sales_order",
        "staff",
        "currency",
        "counterparty",
        "address",
        "department",
        "purchase_order",
        "payment_type",
        "payment",
        "transaction",
    ]
    sync_timestamp = '2024-11-14 08:30:00.000'
   
    result = get_latest_data(conn, tables, sync_timestamp)

    assert isinstance(result, dict) # TODO: # Test query results on test database (filtered data by last update)

def test_get_latest_data_returns_empty_tables_for_the_future_date():
    secret = get_secret('totes-database')
    conn = create_conn(secret)
    tables = [
        "design",
        "sales_order",
        "staff",
        "currency",
        "counterparty",
        "address",
        "department",
        "purchase_order",
        "payment_type",
        "payment",
        "transaction",
    ]

    future_timestamp = datetime.now() + timedelta(days=1)
   
    result = get_latest_data(conn, tables, future_timestamp)

    for table in tables:
        assert result[table] == []
    