import pandas as pd


def convert_dictionary_to_dataframe(data_dict):
    try:
        new_dict = {}
        for table in data_dict:
            new_dict[table] = pd.DataFrame(data_dict[table])
        print('Dict converted to DataFrame')
        return new_dict
    except Exception as e:
        print(f"Error: {e}")
