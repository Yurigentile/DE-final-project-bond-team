from src.datetime_utilities import create_object_with_datetime_key as cod
import re


def test_create_object_with_datetime_key_is_valid_path():
    # Invoke the function
    test_function = cod("extract")

    # Use regex to create a pattern for folder name, iso datetime format and json extension
    match = r"^extract/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}\.json$"

    # Assert to verify output
    assert re.match(match, test_function) is not None


def test_create_object_with_datetime_key_for_uniqueness():
    # Invoke the function
    test_function_with_key1 = cod("extract")
    # Invoke the function again
    test_function_with_key2 = cod("extract")

    # Assert the returned keys are different
    assert test_function_with_key1 != test_function_with_key2


def test_create_object_with_datetime_key_aws_compatibility():
    # Invoke the function
    test_function = cod("extract")

    # Assert correct separator aws
    assert "/" in test_function
    # Assert non compatible separator doesn't exist
    assert "\\" not in test_function
