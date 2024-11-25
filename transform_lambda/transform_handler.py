import logging
import os

if os.environ.get("AWS_EXECUTION_ENV") is not None:
    # For use in lambda function
    from src.load_new_data import load_new_data
    from src.convert_to_dataframe import convert_dictionary_to_dataframe
    from src.df_to_parquet import convert_dataframe_to_parquet
    from src.transform_star import (
    transform_counterparty,
    transform_design,
    transform_sales_order,
    transform_staff, 
    transform_date,
    transform_currency,
    transform_location
) 

else:
    # For local use
    from transform_lambda.src.load_new_data import load_new_data
    from transform_lambda.src.convert_to_dataframe import convert_dictionary_to_dataframe
    from transform_lambda.src.df_to_parquet import convert_dataframe_to_parquet
    from transform_lambda.src.transform_star import (
    transform_counterparty,
    transform_design,
    transform_sales_order,
    transform_staff, 
    transform_date,
    transform_currency,
    transform_location
) 

# EVENT/CONTEXT
    # triggered off previous lambda function's completion
    # event includes data bucket name and processed bucket name

def lambda_handler(event, context):
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)


        data_bucket = event.get("data_bucket")
        processed_bucket = event.get("processed_bucket")

        logger.info("Passed event: data_bucket=%s, processed_bucket=%s", data_bucket, processed_bucket)

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

        # load new JSON files from data bucket + return nested dictionary
        extracted_data_dict = load_new_data(data_bucket, tables)

        # convert dictionaries inside extracted_data_dict into dataframes
        if extracted_data_dict:
            extracted_data_df = convert_dictionary_to_dataframe(extracted_data_dict)
        else:
            print('nothing in dictionary')
            return 

        # create a blank dict to store the transformed dataframes 
        transformed_data_df = {}

        # invoke each transform function, passing the relevant dataframe from extracted_data_df as an arg and saving this as a value on a key in transformed_dfs

        transformed_data_df['dim_design'] = transform_design(extracted_data_df['design'])
        transformed_data_df['dim_currency'] = transform_currency(extracted_data_df['currency'])
        transformed_data_df['dim_counterparty'] = transform_counterparty(extracted_data_df['counterparty'], extracted_data_df['address'])
        transformed_data_df['dim_location'] = transform_location(extracted_data_df['address'])
        transformed_data_df['dim_staff'] = transform_staff(extracted_data_df['staff'], extracted_data_df['department'])
        transformed_data_df['fact_sales_order'] = transform_sales_order(extracted_data_df['sales_order'])
        transformed_data_df['dim_date'] = transform_date(transformed_data_df['fact_sales_order'])

        # loop through the dataframes in transformed_dfs, passing the table name, dataframe & target bucket into convert_dataframes_to_parquet to be convert to parquet and save to processed bucket
        for table_name, dataframe in transformed_data_df.items():
            convert_dataframe_to_parquet(table_name, dataframe, processed_bucket)
            
    except Exception as e:
        logger.info(e)
