from datetime import datetime
import boto3


def create_object_with_datetime_key(folder):
    """
    Generates a file path with a datetime-based key for a JSON file.

    This function takes a folder path and appends a datetime string (in ISO format)
    to the folder path, followed by the '.json' file extension. The datetime string
    represents the current time at which the function is called.

    Args:
        folder (str): The folder path where the JSON file will be created.

    Returns:
        str: A complete file path, combining the folder path and a datetime-based
             key for the JSON file.

    Example:
        create_object_with_datetime_key("/data/files")
        # Returns something like: "/data/files/2024-11-13T12:34:56.789123.json"
    """
    return f"{folder}/{datetime.now().isoformat()}.json"


def retrieve_list_of_s3_files(bucket):
    """
    List all file names in an Amazon S3 bucket.

    This function retrieves and returns the names of all objects stored in the specified
    Amazon S3 bucket. If the bucket is empty, an empty list is returned.

    Parameters:
        bucket_name (str): The name of the S3 bucket to retrieve file names from.

    Returns:
        list: A list of file names (str) in the bucket. Returns an empty list if the bucket
              contains no files.

    Example:
        >>> etrieve_list_of_s3_files('my-bucket')
        ['file1.json', 'file2.json', 'file3.json']

    Raises:
        botocore.exceptions.NoCredentialsError: If AWS credentials are not available.
        botocore.exceptions.ClientError: For other client errors, such as permissions issues.
    """
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket)

    if "Contents" in response:
        return [obj["Key"] for obj in response["Contents"]]
    return []
