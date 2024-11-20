import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import io

def convert_dataframes_to_parquet(table_name, table_df, bucket):
    """
    
    """
    s3_client = boto3.client('s3', region_name = 'eu-west-2')  
    try:
        # Convert the DataFrame to a Parquet file
        table = pa.Table.from_pandas(table_df)

        # Prepare the Parquet file to upload
        parquet_buffer = io.BytesIO()
        pq.write_table(table, parquet_buffer)
        parquet_buffer.seek(0)

        # Prepare key name for s3 object
        s3_key = f'{table_name}-timestamp'

        # Upload parquet file to S3 Bucket
        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=parquet_buffer.getvalue(),
            ContentType='application/json'
        )
        print(f"Saved to {bucket}/{s3_key}")
    except Exception as e:
        print(f"Error: {e}")