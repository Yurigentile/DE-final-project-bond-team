import logging
import os

if os.environ.get("AWS_EXECUTION_ENV") is not None:
    # For use in lambda function
    from src.load_new_data import load_new_data
    from src.convert_to_dataframe import convert_dictionary_to_dataframe
    from src.df_to_parquet import convert_dataframes_to_parquet

else:
    # For local use
    from transform_lambda.src.load_new_data import load_new_data
    from transform_lambda.src.convert_to_dataframe import convert_dictionary_to_dataframe
    from transform_lambda.src.df_to_parquet import convert_dataframes_to_parquet

# EVENT/CONTEXT
    # triggered off previous lambda function's completion? Or files uploaded to S3 bucket? 
    # event includes data bucket name and processed bucket name

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    data_bucket = event.get("data_bucket")
    processed_bucket = event.get("processed_bucket")

    # load new JSON files from data bucket + return nested dictionary
    extracted_data_dict = load_new_data(data_bucket)

    # convert dictionaries inside extracted_data_dict into dataframes
    extracted_data_df = convert_dictionary_to_dataframe(extracted_data_dict)

    # create a blank dict to store the transformed dataframes 
    transformed_data_df = {}

    # invoke each transform function, passing the relevant dataframe from extracted_data_df as an arg and saving this as a value on a key in transformed_dfs
    transformed_data_df['sales_order_fact'] = EXAMPLE___transform_sales_order(extracted_data_df['sales_order'])

    # loop through the dataframes in transformed_dfs, passing the table name, dataframe & target bucket into convert_dataframes_to_parquet to be convert to parquet and save to processed bucket
    for table_name, dataframe in transformed_data_df.items():
        convert_dataframes_to_parquet(table_name, dataframe, processed_bucket)