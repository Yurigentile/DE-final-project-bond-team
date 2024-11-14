import boto3
import json
import logging
from src.s3_save_utilities import s3_save_as_json
from src.s3_helpers import retrieve_list_of_s3_files, create_object_with_datetime_key

def lambda_handler(event, context):
    """
    AWS Lambda Handler to extract data from a database and upload to S3
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    logger.info("Passed event: task=%s, bucket=%s", event.get("task"), event.get("bucket"))
    task = event.get("task")
    folder = event.get("folder", "default_folder")

    # print(f"Task: {task}, Folder: {folder}")
    # if task == "format_key_for_upload":
    #     create_object_with_datetime_key(folder)   
    if task == 'upload_to_s3':
        data = event.get("data", {})
        bucket = event.get("bucket")
        key = event.get("key")
        return s3_save_as_json(data, bucket, key)
    elif task == 'retrieve_files':
        bucket = event.get("bucket")
        return retrieve_list_of_s3_files(bucket)
    else:
        logger.error("Unknown task: %s", task)
        return {'body': 'Unknown task'}