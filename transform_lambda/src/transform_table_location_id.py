
def transform_location(df):
    '''
    This function changes the name of the first column of any given dataframe.
    ARGS:address dataframe
    RETURN: modified and reduced dataframe
    '''
    dim_location = df.copy()
    dim_location = dim_location.rename(columns = {"address_id":"location_id"})
    return dim_location[["location_id","address_line_1","address_line_2","district","city","postal_code","country","phone"]]