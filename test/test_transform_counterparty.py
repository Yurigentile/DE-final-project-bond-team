import pandas as pd
from transform_lambda.src.transform_counterparty import transform_counterparty
import pytest

def test_transform_counterparty():
    input_counterparty_df = pd.DataFrame([
        {
            "counterparty_id": 1,
            "counterparty_legal_name": "Mraz LLC",
            "legal_address_id": 1,
            "commercial_contact": "Jane Wiza",
            "delivery_contact": "Myra Kovacek",
            "created_at": "2022-11-03 14:20:51.563",
            "last_updated": "2022-11-03 14:20:51.563"
        },
        {
            "counterparty_id": 2,
            "counterparty_legal_name": "Frami, Yundt and Macejkovic",
            "legal_address_id": 2,
            "commercial_contact": "Homer Mitchell",
            "delivery_contact": "Ivan Balistreri",
            "created_at": "2022-11-03 14:20:51.563",
            "last_updated": "2022-11-03 14:20:51.563"
        },
        {
            "counterparty_id": 3,
            "counterparty_legal_name": "Alpha",
            "legal_address_id": 2,
            "commercial_contact": "Jhon Doe",
            "delivery_contact": "Mr Python",
            "created_at": "2022-11-03 14:20:51.563",
            "last_updated": "2022-11-03 14:20:51.563"
        }
    ])
        
    input_address_df = pd.DataFrame([
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
            "last_updated": "2022-11-03 14:20:49.962"
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
            "last_updated": "2022-11-03 14:20:49.962"
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
            "last_updated": "2022-11-03 14:20:49.962"
        }
    ])

    expected_df = pd.DataFrame([
        {
            "counterparty_id": 1,
            "counterparty_legal_name": "Mraz LLC",
            "counterparty_legal_address_line_1": "34177 Upton Track",
            "counterparty_legal_address_line_2": "Tremaine Circles",
            "counterparty_legal_district": None,
            "counterparty_legal_city": "Aliso Viejo",
            "counterparty_legal_postal_code": "99305-7380",
            "counterparty_legal_country":  "San Marino",
            "counterparty_legal_phone_number": "9621 880720"
        },
        {
            "counterparty_id": 2,
            "counterparty_legal_name": "Frami, Yundt and Macejkovic",
            "counterparty_legal_address_line_1": "75653 Ernestine Ways",
            "counterparty_legal_address_line_2": None,
            "counterparty_legal_district": "Buckinghamshire ",
            "counterparty_legal_city": "North Deshaun",
            "counterparty_legal_postal_code": "02813",
            "counterparty_legal_country":  "Faroe Islands",
            "counterparty_legal_phone_number": "1373 796260"
        },
        {
            "counterparty_id": 3,
            "counterparty_legal_name": "Alpha",
            "counterparty_legal_address_line_1": "75653 Ernestine Ways",
            "counterparty_legal_address_line_2": None,
            "counterparty_legal_district": "Buckinghamshire ",
            "counterparty_legal_city": "North Deshaun",
            "counterparty_legal_postal_code": "02813",
            "counterparty_legal_country":  "Faroe Islands",
            "counterparty_legal_phone_number": "1373 796260"
        },
    ])
    transformed_df = transform_counterparty(input_counterparty_df, input_address_df)
    pd.testing.assert_frame_equal(transformed_df, expected_df)

def test_transform_counterparty_if_empty_df():
    input_df_1 = pd.DataFrame()
    input_df_2 = pd.DataFrame()
    expected_df = pd.DataFrame()
    
    transformed_df = transform_counterparty(input_df_1, input_df_2)
    pd.testing.assert_frame_equal(transformed_df, expected_df)

def test_transform_design_if_invalid_df_were_given():
    input_df_1 = pd.DataFrame([
        {
            "invalid_column": 472,
            "invalid_column": 123
        }
    ])
    input_df_2 = pd.DataFrame([
        {
            "invalid_column": 472,
            "invalid_column": 123
        }
    ])
    
    with pytest.raises(KeyError, match="Missing required columns"):
        transform_counterparty(input_df_1,input_df_2)