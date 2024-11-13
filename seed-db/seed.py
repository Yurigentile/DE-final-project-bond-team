from src.db_connection import create_conn, close_conn
import json
import os
from dotenv import load_dotenv


def seed():
    load_dotenv()
    credentials = {
        "host": os.getenv("PG_HOST"),
        "user": os.getenv("PG_USER"),
        "password": os.getenv("PG_PASSWORD"),
        "database": os.getenv("PG_DATABASE"),
        "port": os.getenv("PG_PORT")
    }
    
    db = create_conn(json.dumps(credentials))
    print(db)

    try:
        db.run(
            "DROP TABLE IF EXISTS sales_order;"
        )
        db.run(
            "DROP TABLE IF EXISTS transaction;"
        )
        db.run(
            "DROP TABLE IF EXISTS design;"
        )
        db.run(
            """CREATE TABLE sales_order (
                    sales_order_id INT,
                    created_at TIMESTAMP,
                    last_updated TIMESTAMP,
                    design_id INT,
                    staff_id INT,
                    counterparty_id INT,
                    units_sold INT,
                    unit_price NUMERIC,
                    currency_id INT,
                    agreed_delivery_date VARCHAR,
                    agreed_payment_date VARCHAR,
                    agreed_delivery_location_id INT
            );"""
        )
        db.run(
            """CREATE TABLE transaction (
                    transaction_id INT,
                    transaction_type VARCHAR,
                    sales_order_id INT,
                    purchase_order_id INT,
                    created_at TIMESTAMP,
                    last_updated TIMESTAMP
            );"""
        )
        db.run(
            """CREATE TABLE design (
                    design_id INT,
                    created_at TIMESTAMP,
                    last_updated TIMESTAMP,
                    design_name VARCHAR,
                    file_location VARCHAR,
                    file_name VARCHAR
            );"""
        )
        db.run(
            """INSERT INTO sales_order
                        (
                    sales_order_id,
                    created_at,
                    last_updated,
                    design_id,
                    staff_id,
                    counterparty_id,
                    units_sold,
                    unit_price,
                    currency_id,
                    agreed_delivery_date,
                    agreed_payment_date,
                    agreed_delivery_location_id
            )
            VALUES
            (1, '2022-10-11 19:50:33.986000', '2022-10-11 19:50:33.986000', 1, 32, 2, 40011, 4.60, 3, '2022-12-15', '2022-12-16', 14),
            (2, '2022-01-01 01:23:59.186000', '2022-01-01 01:23:59.186000', 5, 15, 1, 40002, 1.94, 2, '2022-11-01', '2022-11-02', 8),
            (3, '2022-02-03 11:15:24.246000', '2022-02-03 11:15:24.246000', 9, 18, 2, 40003, 3.45, 1, '2022-11-05', '2022-11-06', 9),
            (4, '2022-03-04 14:18:31.456000', '2022-03-04 14:18:31.456000', 3, 21, 3, 40004, 5.67, 2, '2022-11-10', '2022-11-12', 7),
            (5, '2022-04-05 09:21:45.786000', '2022-04-05 09:21:45.786000', 6, 25, 1, 40005, 2.30, 3, '2022-11-15', '2022-11-16', 8),
            (6, '2022-05-06 18:27:39.986000', '2022-05-06 18:27:39.986000', 8, 28, 4, 40006, 4.75, 2, '2022-11-20', '2022-11-21', 10),
            (7, '2022-06-07 20:30:21.546000', '2022-06-07 20:30:21.546000', 7, 19, 2, 40007, 3.85, 1, '2022-11-25', '2022-11-26', 11),
            (8, '2022-07-08 15:35:48.126000', '2022-07-08 15:35:48.126000', 2, 22, 3, 40008, 6.15, 3, '2022-12-01', '2022-12-02', 12),
            (9, '2022-08-09 12:40:15.326000', '2022-08-09 12:40:15.326000', 4, 26, 1, 40009, 1.50, 1, '2022-12-05', '2022-12-06', 9),
            (10, '2022-09-10 08:45:22.686000', '2022-09-10 08:45:22.686000', 10, 30, 5, 40010, 7.45, 2, '2022-12-10', '2022-12-11', 13);
             """
        )

        db.run(
            """INSERT INTO transaction
                        (
                    transaction_id,
                    transaction_type,
                    sales_order_id,
                    purchase_order_id,
                    created_at,
                    last_updated
            )
            VALUES
            (1, 'PURCHASE', NULL, 2, '2022-11-03 14:20:52.186000', '2022-11-03 14:20:52.186000'),
            (2, 'SALE', 3, NULL, '2022-11-04 09:15:22.256000', '2022-11-04 09:15:22.256000'),
            (3, 'PURCHASE', NULL, 4, '2022-11-05 10:12:33.186000', '2022-11-05 10:12:33.186000'),
            (4, 'SALE', 5, NULL, '2022-11-06 16:40:45.786000', '2022-11-06 16:40:45.786000'),
            (5, 'PURCHASE', NULL, 6, '2022-11-07 08:33:52.186000', '2022-11-07 08:33:52.186000'),
            (6, 'SALE', 7, NULL, '2022-11-08 14:28:39.926000', '2022-11-08 14:28:39.926000'),
            (7, 'PURCHASE', NULL, 8, '2022-11-09 11:45:15.346000', '2022-11-09 11:45:15.346000'),
            (8, 'SALE', 9, NULL, '2022-11-10 15:50:24.496000', '2022-11-10 15:50:24.496000'),
            (9, 'PURCHASE', NULL, 10, '2022-11-11 10:35:12.216000', '2022-11-11 10:35:12.216000'),
            (10, 'SALE', 11, NULL, '2022-11-12 17:22:18.856000', '2022-11-12 17:22:18.856000');
             """
        )

        db.run(
            """INSERT INTO design
                        (
                    design_id,
                    created_at,
                    last_updated,
                    design_name,
                    file_location,
                    file_name
            )
            VALUES
            (1, '2023-03-04 12:30:21.452000', '2023-03-04 12:30:21.452000', 'Maple', '/var/tmp', 'maple-20230304-a1b2.json'),
            (2, '2022-10-15 08:45:52.736000', '2022-10-15 08:45:52.736000', 'Copper', '/opt/files', 'copper-20221015-x9y8.json'),
            (3, '2023-01-28 17:20:10.154000', '2023-01-28 17:20:10.154000', 'Aluminum', '/usr/local/bin', 'aluminum-20230128-t4v5.json'),
            (4, '2022-12-20 09:15:42.126000', '2022-12-20 09:15:42.126000', 'Silk', '/home/user/data', 'silk-20221220-w3n4.json'),
            (5, '2023-02-11 13:55:08.782000', '2023-02-11 13:55:08.782000', 'Leather', '/srv/www', 'leather-20230211-k2l7.json'),
            (6, '2022-09-05 06:20:33.415000', '2022-09-05 06:20:33.415000', 'Iron', '/mnt/disk', 'iron-20220905-z5r2.json'),
            (7, '2023-04-07 22:12:14.631000', '2023-04-07 22:12:14.631000', 'Marble', '/media/storage', 'marble-20230407-j8u9.json'),
            (8, '2023-03-19 14:32:27.903000', '2023-03-19 14:32:27.903000', 'Wool', '/backup/data', 'wool-20230319-q3m6.json'),
            (9, '2023-05-02 11:10:05.567000', '2023-05-02 11:10:05.567000', 'Glass', '/opt/backup', 'glass-20230502-v6k8.json'),
            (10, '2022-08-24 16:45:50.312000', '2022-08-24 16:45:50.312000', 'Ceramic', '/tmp/files', 'ceramic-20220824-d2b5.json');
             """
        )

    finally:
        print("Seeding Complete")
        close_conn(db)


seed()