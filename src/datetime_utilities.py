from datetime import datetime


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
