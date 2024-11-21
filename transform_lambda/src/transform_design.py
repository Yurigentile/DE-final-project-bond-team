import pandas as pd

def transform_design(design_df):
    """
    Transform loaded design data into star schema
        - remove unwanted columns

    Args:
        design_df (pandas dataframe): original data

    Returns:
        new transformed dataframe
    """
    dim_design = design_df.copy()
    return dim_design[["design_id", "design_name", "file_location", "file_name"]]


