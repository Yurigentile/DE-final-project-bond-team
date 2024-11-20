from transform_lambda.src.convert_to_dataframe import convert_dictionary_to_dataframe
import pandas as pd
import pytest
import unittest


data = {'address': [],
 'counterparty': [],
 'currency': [],
 'department': [],
 'design': [],
 'payment': [{'company_ac_number': 77980960,
              'counterparty_ac_number': 78566145,
              'counterparty_id': 17,
              'created_at': '2024-11-19T12:20:10.216000',
              'currency_id': 2,
              'last_updated': '2024-11-19T12:20:10.216000',
              'paid': False,
              'payment_amount': 52444.38,
              'payment_date': '2024-11-19',
              'payment_id': 15892,
              'payment_type_id': 1,
              'transaction_id': 15892}],
 'payment_type': [],
 'purchase_order': [],
 'sales_order': [{'agreed_delivery_date': '2024-11-20',
                  'agreed_delivery_location_id': 20,
                  'agreed_payment_date': '2024-11-19',
                  'counterparty_id': 17,
                  'created_at': '2024-11-19T12:20:10.216000',
                  'currency_id': 2,
                  'design_id': 243,
                  'last_updated': '2024-11-19T12:20:10.216000',
                  'sales_order_id': 11229,
                  'staff_id': 7,
                  'unit_price': 2.49,
                  'units_sold': 21062}],
 'staff': [],
 'transaction': [{'created_at': '2024-11-19T12:20:10.216000',
                  'last_updated': '2024-11-19T12:20:10.216000',
                  'purchase_order_id': None,
                  'sales_order_id': 11229,
                  'transaction_id': 15892,
                  'transaction_type': 'SALE'}]}


def xtest_data_type_converted_json():
    output_dataframe = convert_dictionary_to_dataframe(data)
    assert type(output_dataframe) == pd.core.frame.DataFrame

def test_function_returns_dict_of_dataframes_with_multiple_dictionary_input():
    output_dataframe = convert_dictionary_to_dataframe(data)
    assert type(output_dataframe["payment"]) == pd.core.frame.DataFrame
    assert type(output_dataframe["sales_order"]) == pd.core.frame.DataFrame
  
class TestExceptions(unittest.TestCase):
    def test_raises_exception_with_invalid_input(self):
        with self.assertRaises(Exception) as detail:
            convert_dictionary_to_dataframe('invalid_input')
            self.assertEqual(str(detail.exception))
