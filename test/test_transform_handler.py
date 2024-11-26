import unittest
from unittest.mock import patch
from transform_lambda.transform_handler import lambda_handler
import pandas as pd

data_json = [
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
    ]

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

class TestTransformHandler(unittest.TestCase):

    @patch('transform_lambda.transform_handler.load_new_data')
    @patch('transform_lambda.transform_handler.convert_dictionary_to_dataframe')
    def test_handler_calls_utility_functions(self, mock_convert_dictionary_to_dataframe, mock_load_new_data):
        
        # mock util functions
        mock_load_new_data.return_value = {"design": data_json}
        mock_convert_dictionary_to_dataframe.return_value = {"design": pd.DataFrame(data_json)}

        # mock event
        mock_event = {
            "data_bucket": "test_data_bucket",
            "processed_bucket": "test_processed_bucket"
        }

        # invoke handler function
        lambda_handler(mock_event, None)

        # assertions
        mock_load_new_data.assert_called_once_with("test_data_bucket", tables)
        mock_convert_dictionary_to_dataframe.assert_called_once_with({"design": data_json})