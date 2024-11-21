import pandas as pd

def transform_staff(df_staff, df_department):

    """
    Transform loaded staff data into star schema
        - remove unwanted columns
        - merged two dataframes
    Args:
        df_staff (staff dataframe): original data for staff
        df_department (department dataframe): original data for department
    Returns:
        data (pandas dataframe): transformed data
    """

    dim_staff = pd.merge(df_staff, df_department, on='department_id')
    return dim_staff[["staff_id", "first_name", "last_name", "department_name", "location", "email_address"]]



def transform_date(df):

    """
    Creating dim_date table into star schema
    Args:
        df (fact_sales_order dataframe): original data
    Returns:
        data (pandas dataframe): transformed data
    """

    dim_date = pd.DataFrame()

    dates_list = ['created_date', 'last_updated_date', 'agreed_payment_date',
                   'agreed_delivery_date']
    for date in dates_list:
        df[date] = pd.to_datetime(df[date])

    dates = pd.melt(df, value_vars=dates_list, value_name='date')
    dim_date['date_id'] = dates[['date']].drop_duplicates().reset_index(drop=True)

    dim_date['year'] = dim_date['date_id'].dt.year.astype('int64') 
    dim_date['month'] = dim_date['date_id'].dt.month.astype('int64') 
    dim_date['day'] = dim_date['date_id'].dt.day.astype('int64') 
    dim_date['day_of_week'] = dim_date['date_id'].dt.dayofweek.astype('int64')
    dim_date['day_name'] = dim_date['date_id'].dt.day_name()
    dim_date['month_name'] = dim_date['date_id'].dt.month_name()
    dim_date['quarter'] = dim_date['date_id'].dt.quarter.astype('int64')
    
    #print(dim_date)
    return dim_date



