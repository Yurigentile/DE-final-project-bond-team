import json
import boto3
import os
import tempfile
import csv
from extract_lambda.src.custom_json_serialiser import custom_json_serializer

def s3_save_as_json(data, bucket, key):
    """
    Saves data to an S3 bucket as a JSON file. 

    Parameters:
    - data (dict): The data to be saved to the S3 bucket. This should be in dictionary format,
      which will be converted to JSON.
    - bucket (str): The name of the S3 bucket where the data will be saved.
    - key (str): The key (path/filename) for the JSON object within the S3 bucket.

    Returns:
    - None

    Raises:
    - Exception: Any exception raised by boto3's put_object function will be caught, printed, and re-raised.

    Side Effects:
    - Outputs a success message if data is saved successfully or an error message if an exception occurs.

    Example:
    >>> data = {"example": "data"}
    >>> bucket = "my-s3-bucket"
    >>> key = "path/to/object.json"
    >>> s3_save(data, bucket, key)
    Saved to my-s3-bucket/path/to/object.json
    """ 
    s3_client = boto3.client('s3', region_name = 'eu-west-2')  
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(data, default=custom_json_serializer),
            ContentType='application/json'
        )
        print(f"Saved to {bucket}/{key}")
    except Exception as e:
        print(f"Error: {e}")

def s3_save_as_csv(data, headers, bucket, key):
    """
    Converts data to CSV, saves it to a temporary file, 
    and uploads it to S3.

    Parameters:
    - data: List of tuples or lists with query result rows.
    - headers: List of column names as strings.
    - bucket: Name of the S3 bucket.
    - key: The S3 object key for the file location.
    """
    s3_client = boto3.client('s3', region_name = 'eu-west-2')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_path = temp_file.name
        
        with open(temp_path, mode='w', newline='') as f:
            csv_writer = csv.writer(f, lineterminator='\n')
            csv_writer.writerow(headers)
            csv_writer.writerows(data)

    with open(temp_path, "rb") as f:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=f,
            ContentType='text/csv'
        )
        print(f"Data saved to {bucket}/{key}")

    os.remove(temp_path)        