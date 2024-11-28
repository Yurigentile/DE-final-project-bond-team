import pandas as pd


def convert_dictionary_to_dataframe(data_dict):
    """
    Takes a nested dictionary with dictionaries stored as values, and returns a new nested dictionary where values have been converted into DataFrames

    Parameters:
        data_dict (dict): dictionary object with table names as keys, and dictionaries as values

    Returns:
        new dictionary with table names as keys, and DataFrames as values

    Side Effects:
        On failure - Exception printed to console

    Example:
        >>> convert_dictionary_to_dataframe({'example_table': {'dict_1': 12345}})
        Returns {'example_table': [DataFrame]}
    """
    try:
        new_dict = {}
        for table in data_dict:
            new_dict[table] = pd.DataFrame(data_dict[table])
        print('Dict converted to DataFrame')
        return new_dict
    except Exception as e:
        print(f"Error: {e}")
