import pandas as pd

def transform_design(design_df):
    """
    Transform loaded design data into star schema
        - removes unwanted columns

    Args:
        design_df (pandas dataframe): original data

    Returns:
        new transformed dataframe

    Side Effects:
    - Outputs "The input dataframe is empty." message if input dataframe were an empty.

    """
    if design_df.empty:
        print("The input dataframe is empty.")
        return design_df

    try:    
        dim_design = design_df.copy()
        return dim_design[["design_id", "design_name", "file_location", "file_name"]]
    except KeyError as e:
        raise KeyError(f"Missing required columns: {e}")
