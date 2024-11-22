#from currency_codes import get_currency_by_code



def transform_currency(df):
    ''' 
    This function uses get_currency_by_code library in order to get a currency name by its international
    code, in order to test it we compared 2 pandas dataframes.
    This function removes unneeded columns.
    ARGS: currency dataframe:original data,
    RETURNS: transformed dataframe
'''
    dim_currency = df.copy()
    currency_codes = list(dim_currency['currency_code'])
    #dim_currency['currency_name'] = [get_currency_by_code(code).name for code in currency_codes]
    return dim_currency[['currency_id','currency_code','currency_name']]