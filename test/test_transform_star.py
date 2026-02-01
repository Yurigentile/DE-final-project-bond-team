import pandas as pd
from lambda_transform.src.transform_star import (
    transform_counterparty,
    transform_design,
    transform_sales_order,
    transform_staff,
    transform_date,
    transform_currency,
    transform_location,
)
from datetime import datetime
import pytest


def test_transform_counterparty():
    input_counterparty_df = pd.DataFrame(
        [
            {
                "counterparty_id": 1,
                "counterparty_legal_name": "Mraz LLC",
                "legal_address_id": 1,
                "commercial_contact": "Jane Wiza",
                "delivery_contact": "Myra Kovacek",
                "created_at": "2022-11-03 14:20:51.563",
                "last_updated": "2022-11-03 14:20:51.563",
            },
            {
                "counterparty_id": 2,
                "counterparty_legal_name": "Frami, Yundt and Macejkovic",
                "legal_address_id": 2,
                "commercial_contact": "Homer Mitchell",
                "delivery_contact": "Ivan Balistreri",
                "created_at": "2022-11-03 14:20:51.563",
                "last_updated": "2022-11-03 14:20:51.563",
            },
            {
                "counterparty_id": 3,
                "counterparty_legal_name": "Alpha",
                "legal_address_id": 2,
                "commercial_contact": "Jhon Doe",
                "delivery_contact": "Mr Python",
                "created_at": "2022-11-03 14:20:51.563",
                "last_updated": "2022-11-03 14:20:51.563",
            },
        ]
    )

    input_address_df = pd.DataFrame(
        [
            {
                "address_id": 1,
                "address_line_1": "34177 Upton Track",
                "address_line_2": "Tremaine Circles",
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
            {
                "address_id": 2,
                "address_line_1": "75653 Ernestine Ways",
                "address_line_2": None,
                "district": "Buckinghamshire ",
                "city": "North Deshaun",
                "postal_code": "02813",
                "country": "Faroe Islands",
                "phone": "1373 796260",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
            {
                "address_id": 100,
                "address_line_1": "Nobody references this address in counterparty",
                "address_line_2": "Absolutely",
                "district": "Nowhere",
                "city": "Gone",
                "postal_code": "00000",
                "country": "Unknown",
                "phone": "1373 796260",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
        ]
    )

    expected_df = pd.DataFrame(
        [
            {
                "counterparty_id": 1,
                "counterparty_legal_name": "Mraz LLC",
                "counterparty_legal_address_line_1": "34177 Upton Track",
                "counterparty_legal_address_line_2": "Tremaine Circles",
                "counterparty_legal_district": None,
                "counterparty_legal_city": "Aliso Viejo",
                "counterparty_legal_postal_code": "99305-7380",
                "counterparty_legal_country": "San Marino",
                "counterparty_legal_phone_number": "9621 880720",
            },
            {
                "counterparty_id": 2,
                "counterparty_legal_name": "Frami, Yundt and Macejkovic",
                "counterparty_legal_address_line_1": "75653 Ernestine Ways",
                "counterparty_legal_address_line_2": None,
                "counterparty_legal_district": "Buckinghamshire ",
                "counterparty_legal_city": "North Deshaun",
                "counterparty_legal_postal_code": "02813",
                "counterparty_legal_country": "Faroe Islands",
                "counterparty_legal_phone_number": "1373 796260",
            },
            {
                "counterparty_id": 3,
                "counterparty_legal_name": "Alpha",
                "counterparty_legal_address_line_1": "75653 Ernestine Ways",
                "counterparty_legal_address_line_2": None,
                "counterparty_legal_district": "Buckinghamshire ",
                "counterparty_legal_city": "North Deshaun",
                "counterparty_legal_postal_code": "02813",
                "counterparty_legal_country": "Faroe Islands",
                "counterparty_legal_phone_number": "1373 796260",
            },
        ]
    )
    transformed_df = transform_counterparty(input_counterparty_df, input_address_df)
    pd.testing.assert_frame_equal(transformed_df, expected_df)


def test_transform_design_if_invalid_df_were_given():
    input_df_1 = pd.DataFrame([{"invalid_column": 472, "invalid_column": 123}])
    input_df_2 = pd.DataFrame([{"invalid_column": 472, "invalid_column": 123}])

    with pytest.raises(KeyError, match="Missing required columns"):
        transform_counterparty(input_df_1, input_df_2)


""""""


def test_transform_design():
    input_df = pd.DataFrame(
        [
            {
                "design_id": 472,
                "created_at": datetime(2024, 11, 14, 9, 41, 9, 839000),
                "design_name": "Concrete",
                "file_location": "/usr/share",
                "file_name": "concrete-20241026-76vi.json",
                "last_updated": datetime(2024, 11, 14, 9, 41, 9, 839000),
            },
            {
                "design_id": 473,
                "created_at": datetime(2024, 11, 15, 14, 9, 9, 608000),
                "design_name": "Rubber",
                "file_location": "/Users",
                "file_name": "rubber-20240916-1hsu.json",
                "last_updated": datetime(2024, 11, 15, 14, 9, 9, 608000),
            },
        ]
    )

    expected_df = pd.DataFrame(
        [
            {
                "design_id": 472,
                "design_name": "Concrete",
                "file_location": "/usr/share",
                "file_name": "concrete-20241026-76vi.json",
            },
            {
                "design_id": 473,
                "design_name": "Rubber",
                "file_location": "/Users",
                "file_name": "rubber-20240916-1hsu.json",
            },
        ]
    )

    transformed_df = transform_design(input_df)
    pd.testing.assert_frame_equal(transformed_df, expected_df)


def test_transform_design_if_invalid_df_were_given():
    input_df = pd.DataFrame([{"invalid_column": 472, "invalid_column": 123}])

    with pytest.raises(KeyError, match="Missing required columns"):
        transform_design(input_df)


""""""


def test_transform_sales_order():
    input_df = pd.DataFrame(
        [
            {
                "sales_order_id": 1,
                "created_at": "2022-11-03T14:20:52.186",
                "last_updated": "2022-11-03 14:20:52.186",
                "design_id": 2,
                "staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": 3.94,
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-07",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 8,
            },
            {
                "sales_order_id": 2,
                "created_at": "2022-11-03T14:20:52.188",
                "last_updated": "2022-11-03 14:20:52.188",
                "design_id": 3,
                "staff_id": 10,
                "counterparty_id": 4,
                "units_sold": 65839,
                "unit_price": 2.91,
                "currency_id": 3,
                "agreed_delivery_date": "2022-11-06",
                "agreed_payment_date": "2022-11-07",
                "agreed_delivery_location_id": 8,
            },
        ]
    )

    expected_df = pd.DataFrame(
        [
            {
                "sales_record_id": 1,
                "sales_order_id": 1,
                "created_date": pd.to_datetime("2022-11-3"),
                "created_time": "14:20:52.186000",
                "last_updated_date": pd.to_datetime("2022-11-3"),
                "last_updated_time": "14:20:52.186000",
                "sales_staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": 3.94,
                "currency_id": 2,
                "design_id": 2,
                "agreed_payment_date": pd.to_datetime("2022-11-08"),
                "agreed_delivery_date": pd.to_datetime("2022-11-07"),
                "agreed_delivery_location_id": 8,
            },
            {
                "sales_record_id": 2,
                "sales_order_id": 2,
                "created_date": pd.to_datetime("2022-11-3"),
                "created_time": "14:20:52.188000",
                "last_updated_date": pd.to_datetime("2022-11-3"),
                "last_updated_time": "14:20:52.188000",
                "sales_staff_id": 10,
                "counterparty_id": 4,
                "units_sold": 65839,
                "unit_price": 2.91,
                "currency_id": 3,
                "design_id": 3,
                "agreed_payment_date": pd.to_datetime("2022-11-07"),
                "agreed_delivery_date": pd.to_datetime("2022-11-06"),
                "agreed_delivery_location_id": 8,
            },
        ]
    )
    transformed_df = transform_sales_order(input_df)

    pd.testing.assert_frame_equal(transformed_df, expected_df)


""""""


def test_staff_success():
    df_staff = pd.DataFrame(
        {
            "staff_id": [1],
            "first_name": ["A1"],
            "last_name": ["B0"],
            "department_id": [1],
            "extra_info": ["A1"],
            "email_address": ["B0"],
        }
    )

    df_department = pd.DataFrame(
        {
            "department_id": [1],
            "department_name": ["C2"],
            "location": ["D2"],
            "extra_info_2": ["A2"],
        }
    )

    output = pd.DataFrame(
        {
            "staff_id": [1],
            "first_name": ["A1"],
            "last_name": ["B0"],
            "department_name": ["C2"],
            "location": ["D2"],
            "email_address": ["B0"],
        }
    )

    pd.testing.assert_frame_equal(transform_staff(df_staff, df_department), output)


def test_date_success():
    df = pd.DataFrame(
        {
            "created_date": ["2023-11-08"],
            "last_updated_date": ["2024-10-06"],
            "agreed_payment_date": ["2023-11-08"],
            "agreed_delivery_date": ["2023-09-07"],
        }
    )
    output = pd.DataFrame(
        {
            "date_id": pd.to_datetime(["2023-11-8", "2024-10-06", "2023-09-07"]),
            "year": [2023, 2024, 2023],
            "month": [11, 10, 9],
            "day": [8, 6, 7],
            "day_of_week": [2, 6, 3],  # 3 if without 0-indexing
            "day_name": ["Wednesday", "Sunday", "Thursday"],
            "month_name": ["November", "October", "September"],
            "quarter": [4, 4, 3],
        }
    )

    pd.testing.assert_frame_equal(transform_date(df), output)


""""""


def test_transform_table_with_single_currency():
    currency_df_input = pd.DataFrame(
        [
            {
                "currency_id": 1,
                "currency_code": "GBP",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
            {
                "currency_id": 2,
                "currency_code": "USD",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
            {
                "currency_id": 3,
                "currency_code": "EUR",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
        ]
    )
    expected_df = pd.DataFrame(
        [
            {
                "currency_id": 1,
                "currency_code": "GBP",
                "currency_name": "Pound Sterling",
            },
            {"currency_id": 2, "currency_code": "USD", "currency_name": "US Dollar"},
            {"currency_id": 3, "currency_code": "EUR", "currency_name": "Euro"},
        ]
    )

    transformed_df = transform_currency(currency_df_input)
    pd.testing.assert_frame_equal(transformed_df, expected_df)


""""""


def test_transform_table_location_id():
    input_address_df = pd.DataFrame(
        [
            {
                "address_id": 1,
                "address_line_1": "34177 Upton Track",
                "address_line_2": "Tremaine Circles",
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
            {
                "address_id": 2,
                "address_line_1": "75653 Ernestine Ways",
                "address_line_2": None,
                "district": "Buckinghamshire ",
                "city": "North Deshaun",
                "postal_code": "02813",
                "country": "Faroe Islands",
                "phone": "1373 796260",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
            {
                "address_id": 100,
                "address_line_1": "Nobody references this address in counterparty",
                "address_line_2": "Absolutely",
                "district": "Nowhere",
                "city": "Gone",
                "postal_code": "00000",
                "country": "Unknown",
                "phone": "1373 796260",
                "created_at": "2022-11-03 14:20:49.962",
                "last_updated": "2022-11-03 14:20:49.962",
            },
        ]
    )
    expected_df = pd.DataFrame(
        [
            {
                "location_id": 1,
                "address_line_1": "34177 Upton Track",
                "address_line_2": "Tremaine Circles",
                "district": None,
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720",
            },
            {
                "location_id": 2,
                "address_line_1": "75653 Ernestine Ways",
                "address_line_2": None,
                "district": "Buckinghamshire ",
                "city": "North Deshaun",
                "postal_code": "02813",
                "country": "Faroe Islands",
                "phone": "1373 796260",
            },
            {
                "location_id": 100,
                "address_line_1": "Nobody references this address in counterparty",
                "address_line_2": "Absolutely",
                "district": "Nowhere",
                "city": "Gone",
                "postal_code": "00000",
                "country": "Unknown",
                "phone": "1373 796260",
            },
        ]
    )

    transformed_df = transform_location(input_address_df)
    pd.testing.assert_frame_equal(transformed_df, expected_df)
