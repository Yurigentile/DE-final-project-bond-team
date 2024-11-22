import unittest
from unittest.mock import patch
from transform_lambda.transform_handler import lambda_handler, transform_function
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
    @patch('transform_lambda.transform_handler.transform_function')
    @patch('transform_lambda.transform_handler.convert_dataframe_to_parquet')
    def test_handler_calls_utility_functions(self, mock_convert_dataframe_to_parquet, mock_transform_function, mock_convert_dictionary_to_dataframe, mock_load_new_data):
        
        mock_load_new_data.return_value = {"table": data_json}
        mock_convert_dictionary_to_dataframe.return_value = {"table": pd.DataFrame(data_json)}
        mock_transform_function.return_value = pd.DataFrame(data_json)
        mock_convert_dataframe_to_parquet.return_value = '{"paths": ["s3://test-bucket/2024-11-20 17:57:20/payment.parquet"], "partitions_values": []}'

        mock_event = {
            "data_bucket": "test_data_bucket",
            "processed_bucket": "test_processed_bucket"
        }

        lambda_handler(mock_event, None)

        mock_load_new_data.assert_called_once_with("test_data_bucket", tables)
        mock_convert_dictionary_to_dataframe.assert_called_once_with({"table": data_json})
        mock_transform_function.assert_called_once_with('mock_dataframe')
        mock_convert_dataframe_to_parquet.assert_called_once_with(
            'table', pd.DataFrame(data_json), 'test_processed_bucket'
        )