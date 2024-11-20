import awswrangler as wr
from datetime import datetime
from transform_lambda.src.convert_to_dataframe import convert_dictionary_to_dataframe


def convert_dataframe_to_parquet(table_name, table_df, bucket):
    """
    Save a dataframe to s3 bucket

    This function retrieves a desired table_name, dataframe, and s3 bucket name, converts the dataframe to parquet file format and uploads this file to the bucket using awswrangler.

    Parameters:
        table_name (str): The name of the table which you want to 
        table_df (DataFrame): The DataFrame object which you want to convert to parquet
        bucket (str): The name of the S3 bucket you want to upload the file to

    Returns:
        Nothing

    Side Effects:
        On success - Parquet file added to S3 bucket
        On failure - Exception printed to console

    Example:
        >>> convert_dataframe_to_parquet('example_table', dataframe, 'example-bucket')
        Print - Saved to s3://{bucket-name/timestamp/table-name}.parquet
    """
    try:
        # creates current timestamp for s3 file name
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # set the desired location for the parquet file
        path = f"s3://{bucket}/{current_timestamp}/{table_name}.parquet"

        # convert the DataFrame to parquet and save to path in s3 bucket
        wr.s3.to_parquet(table_df, path)

        print(f"Saved to {path}")
    except Exception as e:
        print(f"Error: {e}")

test_data = {'address': [],

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

test_dfs = convert_dictionary_to_dataframe(test_data)

convert_dataframe_to_parquet('payment', test_dfs['payment'], 'nc-project-totes-processed')