from transform_lambda.src.df_to_parquet import convert_dataframe_to_parquet
from transform_lambda.src.convert_to_dataframe import convert_dictionary_to_dataframe
import pytest
from unittest.mock import patch
import unittest

test_dict = {'address': [],

 'counterparty': [],
 'currency': [],
 'department': [],
 'design': [],
 'payment': [{'company_ac_number': 123456,
              'counterparty_ac_number': 123456,
              'counterparty_id': 17,
              'created_at': '2024-11-19T12:20:10.216000',
              'currency_id': 2,
              'last_updated': '2024-11-19T12:20:10.216000',
              'paid': False,
              'payment_amount': 1234.56,
              'payment_date': '2024-11-19',
              'payment_id': 123456,
              'payment_type_id': 1,
              'transaction_id': 123456}],
 'payment_type': [],
 'purchase_order': [],
 'sales_order': [{'agreed_delivery_date': '2024-11-20',
                  'agreed_delivery_location_id': 20,
                  'agreed_payment_date': '2024-11-19',
                  'counterparty_id': 17,
                  'created_at': '2024-11-19T12:20:10.216000',
                  'currency_id': 2,
                  'design_id': 123,
                  'last_updated': '2024-11-19T12:20:10.216000',
                  'sales_order_id': 123456,
                  'staff_id': 7,
                  'unit_price': 2.49,
                  'units_sold': 123456}],
 'staff': [],
 'transaction': [{'created_at': '2024-11-19T12:20:10.216000',
                  'last_updated': '2024-11-19T12:20:10.216000',
                  'purchase_order_id': None,
                  'sales_order_id': 123456,
                  'transaction_id': 123456,
                  'transaction_type': 'SALE'}]}

class TestDfToParuqet:

    @patch('transform_lambda.src.df_to_parquet.wr.s3.to_parquet')
    def test_function_uploads_file_to_s3_bucket(self, mock_df_to_parquet):
        
        # mock aws wrangler
        mock_df_to_parquet.return_value = '{"paths": ["s3://test-bucket/2024-11-20 17:57:20/payment.parquet"], "partitions_values": []}'
        
        # convert dictionary to DataFrame using util function
        test_df_dict = convert_dictionary_to_dataframe(test_dict)

        # invoke function
        convert_dataframe_to_parquet('payment', test_df_dict['payment'], 'test_bucket')

        # check mock was called correctly
        mock_df_to_parquet.assert_called_once()

class TestException(unittest.TestCase):
    @patch('transform_lambda.src.df_to_parquet.wr.s3.to_parquet')
    @patch('builtins.print')
    def test_function_raises_exception_for_invalid_bucket(self, mock_print, mock_to_parquet):

        # mock exception
        mock_to_parquet.side_effect = Exception("NoSuchBucket")

        # convert dictionary to DataFrame using util function
        test_df_dict = convert_dictionary_to_dataframe(test_dict)

        # invoke function            
        convert_dataframe_to_parquet('payment', test_df_dict['payment'], 'test_bucket')

        # assertion
        mock_print.assert_any_call("Error processing payment: NoSuchBucket")



        