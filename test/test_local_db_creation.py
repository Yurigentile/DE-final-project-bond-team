import pytest
from pg8000.native import Connection
from dotenv import load_dotenv
import os

load_dotenv('.env.test')
@pytest.fixture(scope='module')
def local_db_conn():
    try:
        conn = Connection(
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            timeout=10,
        )
        yield conn
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

# Test for users table
def test_users_table(local_db_conn):
    columns = local_db_conn.run("SELECT column_name FROM information_schema.columns WHERE table_name='users';")
    expected_columns = {'id', 'name', 'email'}
    actual_columns = {column[0] for column in columns}
    assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for products table
def test_products_table(local_db_conn):
    columns = local_db_conn.run("SELECT column_name FROM information_schema.columns WHERE table_name='products';")
    expected_columns = {'id', 'name', 'price'}
    actual_columns = {column[0] for column in columns}
    assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for orders table
def test_orders_table(local_db_conn):
    columns = local_db_conn.run("SELECT column_name FROM information_schema.columns WHERE table_name='orders';")
    expected_columns = {'id', 'user_id', 'order_date'}
    actual_columns = {column[0] for column in columns}
    assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for order_items table
def test_order_items_table(local_db_conn):
    columns = local_db_conn.run("SELECT column_name FROM information_schema.columns WHERE table_name='order_items';")
    expected_columns = {'id', 'order_id', 'product_id', 'quantity'}
    actual_columns = {column[0] for column in columns}
    assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

# Test for reviews table
def test_reviews_table(local_db_conn):
    columns = local_db_conn.run("SELECT column_name FROM information_schema.columns WHERE table_name='reviews';")
    expected_columns = {'id', 'user_id', 'product_id', 'rating', 'comment'}
    actual_columns = {column[0] for column in columns}
    assert expected_columns.issubset(actual_columns), f"Expected columns {expected_columns} but got {actual_columns}"

#Test for user count
def test_user_count(local_db_conn):
    user_count = local_db_conn.run("SELECT COUNT(*) FROM users")[0][0]
    assert user_count == 3, f"Expected 3 users, found {user_count}"

#Test for product count
def test_product_count(local_db_conn):
    product_count = local_db_conn.run("SELECT COUNT(*) FROM products")[0][0]
    assert product_count == 5, f"Expected 5 products, found {product_count}"

#Test for order count
def test_order_count(local_db_conn):
    order_count = local_db_conn.run("SELECT COUNT(*) FROM orders")[0][0]
    assert order_count == 3, f"Expected 3 orders, found {order_count}"

#Test for items count
def test_order_items_count(local_db_conn):
    order_items_count = local_db_conn.run("SELECT COUNT(*) FROM order_items")[0][0]
    assert order_items_count == 5, f"Expected 5 order items, found {order_items_count}"

#Test for review count
def test_review_count(local_db_conn):
    review_count = local_db_conn.run("SELECT COUNT(*) FROM reviews")[0][0]
    assert review_count == 5, f"Expected 5 reviews, found {review_count}"

#Test for alices order
def test_alice_order(local_db_conn):
    alice_order = local_db_conn.run("""
        SELECT oi.product_id, oi.quantity
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        WHERE o.user_id = 1
    """)
    expected_items = [[1, 1], [2, 2]]
    assert alice_order == expected_items, f"Expected {expected_items}, found {alice_order}"

#Test for charlies reviews
def test_charlie_reviews(local_db_conn):
    charlie_reviews = local_db_conn.run("""
        SELECT r.product_id, r.rating, r.comment
        FROM reviews r
        WHERE r.user_id = 3
    """)
    expected_reviews = [
        [4, 5, 'Love the monitor! Crystal clear.'],
        [5, 4, 'Headphones are solid.']
    ]
    assert charlie_reviews == expected_reviews, f"Expected {expected_reviews}, found {charlie_reviews}"