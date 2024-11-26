import unittest
from unittest.mock import patch, Mock, MagicMock
import json
from load_lambda.src.load_parquet_data import read_parquet_data_to_dataframe, retrive_list_of_files
from botocore.exceptions import NoCredentialsError, ClientError
import pandas as pd


class TestReadParquetToDF(unittest.TestCase):
    @patch("load_lambda.src.load_parquet_data.retrive_list_of_files")
    @patch("load_lambda.src.load_parquet_data.wr.s3.read_parquet")
    def test_load_new_data(self, mock_aws_wrangler, mock_retrieve_list):

        # mock dataframe 
        mock_fact_sales_order = pd.DataFrame(
                [
                    {
                        "sales_order_id": 12345,
                        "created_at": "2024-11-19T15:50:10.225000",
                        "last_updated": "2024-11-19T15:50:10.225000",
                        "design_id": 123,
                        "staff_id": 11,
                        "counterparty_id": 11,
                        "units_sold": 12345,
                        "unit_price": 5.77,
                        "currency_id": 1,
                        "agreed_delivery_date": "2024-11-25",
                        "agreed_payment_date": "2024-11-23",
                        "agreed_delivery_location_id": 10
                    }
                    ]
        )

        # mock retrive_list_of_files
        mock_retrieve_list.return_value = [
            "2024-11-25 12:00/fact_sales_order.parquet"
        ]

        # return mock if the table name is fact_sales_order only
        def mock_aws_wrangler_side_effect(path, **kwargs):
            if "fact_sales_order" in path[0]:
                return mock_fact_sales_order
            raise FileNotFoundError

        mock_aws_wrangler.side_effect = mock_aws_wrangler_side_effect

        # invoke function
        bucket_name = "test-bucket"
        result = read_parquet_data_to_dataframe(bucket_name)

        #assertions
        self.assertEqual(result, {'fact_sales_order': mock_fact_sales_order})
        self.assertIn("fact_sales_order", result)
        mock_retrieve_list.assert_called_once_with(bucket_name)