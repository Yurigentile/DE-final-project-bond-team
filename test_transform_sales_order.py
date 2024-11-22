from transform_sales_order import transform_sales_order
import pandas as pd
from datetime import date,time
from decimal import Decimal

def test_transform_sales_order():
    input_df = pd.DataFrame([
        {
            "sales_order_id": 1,
            "created_at": "2022-11-03 14:20:52.186",
            "last_updated": "2022-11-03 14:20:52.186",
            "design_id": 2,
            "staff_id": 19,
            "counterparty_id": 8,
            "units_sold": 42972,
            "unit_price": "3.94",
            "currency_id": 2,
            "agreed_delivery_date": "2022-11-07",
            "agreed_payment_date": "2022-11-08",
            "agreed_delivery_location_id": 8
        },
        {
            "sales_order_id": 2,
            "created_at": "2022-11-03 14:20:52.188",
            "last_updated": "2022-11-03 14:20:52.188",
            "design_id": 3,
            "staff_id": 10,
            "counterparty_id": 4,
            "units_sold": 65839,
            "unit_price": "2.91",
            "currency_id": 3,
            "agreed_delivery_date": "2022-11-06",
            "agreed_payment_date": "2022-11-07",
            "agreed_delivery_location_id": 8
        }
    ])

    expected_df = pd.DataFrame([
        {
            "sales_order_id": 1,
            "created_date": pd.to_datetime("2022-11-3"),
            "created_time": "14:20:52.186000",
            "last_updated_date": pd.to_datetime("2022-11-3"),
            "last_updated_time":"14:20:52.186000",
            "sales_staff_id": 19,  
            "counterparty_id": 8,
            "units_sold": 42972,
            "unit_price": 3.94,
            "currency_id": 2,
            "design_id": 2,
            "agreed_payment_date": pd.to_datetime("2022-11-8"),
            "agreed_delivery_date": pd.to_datetime("2022-11-7"),          
            "agreed_delivery_location_id": 8
        },
        {
            "sales_order_id": 2,
            "created_date": pd.to_datetime("2022-11-3"),
            "created_time": "14:20:52.188000",
            "last_updated_date": pd.to_datetime("2022-11-3"),
            "last_updated_time":"14:20:52.188000",
            "sales_staff_id": 10,  
            "counterparty_id": 4,
            "units_sold": 65839,
            "unit_price": 2.91,
            "currency_id": 2,
            "design_id": 2,
            "agreed_payment_date": pd.to_datetime("2022-11-8"),
            "agreed_delivery_date": pd.to_datetime("2022-11-7"),          
            "agreed_delivery_location_id": 8
        }
    ])
    expected_df.index.name = "sales_record_id"
    expected_df.index = expected_df.index + 1
    transformed_df = transform_sales_order(input_df)

    pd.testing.assert_frame_equal(transformed_df,expected_df)