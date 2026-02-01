import pandas as pd
from currency_codes import get_currency_by_code


def transform_sales_order(sales_order_df):
    """
    Transform loaded sales order data into star schema
        - renames columns
        - splits out timestamp into date and time
    Args:
        df (sales order dataframe): original data
    Returns:
        data (pandas dataframe): transformed data
    """
    if sales_order_df.empty:
        print("transform_sales_order - The input dataframe is empty.")
        return pd.DataFrame(
            columns=[
                "sales_record_id",
                "sales_order_id",
                "created_date",
                "created_time",
                "last_updated_date",
                "last_updated_time",
                "sales_staff_id",
                "counterparty_id",
                "units_sold",
                "unit_price",
                "currency_id",
                "design_id",
                "agreed_payment_date",
                "agreed_delivery_date",
                "agreed_delivery_location_id",
            ]
        )

    try:
        fact_sales_order = sales_order_df.copy()
        fact_sales_order = fact_sales_order.rename(
            columns={"staff_id": "sales_staff_id"}
        )

        # Create 2 Columns for created_at
        fact_sales_order["created_at"] = pd.to_datetime(
            fact_sales_order["created_at"], format="ISO8601"
        )

        fact_sales_order["created_date"] = fact_sales_order[
            "created_at"
        ].dt.date.astype("datetime64[ns]")
        fact_sales_order["created_time"] = fact_sales_order[
            "created_at"
        ].dt.time.astype(str)

        # Create 2 Columns for last_updated
        fact_sales_order["last_updated"] = pd.to_datetime(
            fact_sales_order["last_updated"], format="ISO8601"
        )
        fact_sales_order["last_updated_date"] = fact_sales_order[
            "last_updated"
        ].dt.date.astype("datetime64[ns]")
        fact_sales_order["last_updated_time"] = fact_sales_order[
            "last_updated"
        ].dt.time.astype(str)

        # Convert
        fact_sales_order["agreed_payment_date"] = pd.to_datetime(
            fact_sales_order["agreed_payment_date"]
        )
        fact_sales_order["agreed_payment_date"] = fact_sales_order[
            "agreed_payment_date"
        ].dt.date.astype("datetime64[ns]")

        fact_sales_order["agreed_delivery_date"] = pd.to_datetime(
            fact_sales_order["agreed_delivery_date"]
        )
        fact_sales_order["agreed_delivery_date"] = fact_sales_order[
            "agreed_delivery_date"
        ].dt.date.astype("datetime64[ns]")

        # Create sales_record_id as a column (not index) for database loading
        fact_sales_order = fact_sales_order.reset_index(drop=True)
        fact_sales_order.insert(0, "sales_record_id", fact_sales_order.index + 1)

        fact_sales_order = fact_sales_order[
            [
                "sales_record_id",
                "sales_order_id",
                "created_date",
                "created_time",
                "last_updated_date",
                "last_updated_time",
                "sales_staff_id",
                "counterparty_id",
                "units_sold",
                "unit_price",
                "currency_id",
                "design_id",
                "agreed_payment_date",
                "agreed_delivery_date",
                "agreed_delivery_location_id",
            ]
        ]
        return fact_sales_order
    except Exception as e:
        print(f"transform_sales_order Function: ", {e})


def transform_counterparty(counterparty_df, address_df):
    """
    Transform loaded counterparty data into star schema
        - removes unwanted columns
        - renames columns as in star schema
        - retrieves adress from address data

    Args:
        counterparty_df: original data (pandas dataframe)
        adress_df: original data (pandas dataframe)

    Returns:
        new transformed dataframe

    Side Effects:
    - Outputs "The input dataframe is empty." message if input dataframe were an empty.
    """
    if counterparty_df.empty or address_df.empty:
        print("transform_counterparty - The input dataframe is empty.")
        return pd.DataFrame(
            columns=[
                "counterparty_id",
                "counterparty_legal_name",
                "counterparty_legal_address_line_1",
                "counterparty_legal_address_line_2",
                "counterparty_legal_district",
                "counterparty_legal_city",
                "counterparty_legal_postal_code",
                "counterparty_legal_country",
                "counterparty_legal_phone_number",
            ]
        )

    try:
        dim_counterparty = counterparty_df.copy()
        dim_counterparty = dim_counterparty.merge(
            address_df, how="left", left_on="legal_address_id", right_on="address_id"
        )
        dim_counterparty = dim_counterparty.rename(
            columns={
                "address_line_1": "counterparty_legal_address_line_1",
                "address_line_2": "counterparty_legal_address_line_2",
                "district": "counterparty_legal_district",
                "city": "counterparty_legal_city",
                "postal_code": "counterparty_legal_postal_code",
                "country": "counterparty_legal_country",
                "phone": "counterparty_legal_phone_number",
            }
        )
        return dim_counterparty[
            [
                "counterparty_id",
                "counterparty_legal_name",
                "counterparty_legal_address_line_1",
                "counterparty_legal_address_line_2",
                "counterparty_legal_district",
                "counterparty_legal_city",
                "counterparty_legal_postal_code",
                "counterparty_legal_country",
                "counterparty_legal_phone_number",
            ]
        ]
    except KeyError as e:
        raise KeyError(f"Missing required columns: {e}")


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
        print("transform_design - The input dataframe is empty.")
        return pd.DataFrame(
            columns=["design_id", "design_name", "file_location", "file_name"]
        )

    try:
        dim_design = design_df.copy()
        return dim_design[["design_id", "design_name", "file_location", "file_name"]]
    except KeyError as e:
        raise KeyError(f"Missing required columns: {e}")


def transform_staff(staff_df, department_df):
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
    if staff_df.empty or department_df.empty:
        print("transform_staff - The input dataframe is empty.")
        return pd.DataFrame(
            columns=[
                "staff_id",
                "first_name",
                "last_name",
                "department_name",
                "location",
                "email_address",
            ]
        )

    try:
        dim_staff = pd.merge(staff_df, department_df, on="department_id")
        return dim_staff[
            [
                "staff_id",
                "first_name",
                "last_name",
                "department_name",
                "location",
                "email_address",
            ]
        ]
    except Exception as e:
        print(e)


def transform_date(fact_sales_order_df):
    """
    Creating dim_date table into star schema
    Args:
        df (fact_sales_order dataframe): original data
    Returns:
        data (pandas dataframe): transformed data
    """
    if fact_sales_order_df is None or fact_sales_order_df.empty:
        print("transform_date - The input dataframe is empty.")
        return pd.DataFrame(
            columns=[
                "date_id",
                "year",
                "month",
                "day",
                "day_of_week",
                "day_name",
                "month_name",
                "quarter",
            ]
        )

    try:
        dim_date = pd.DataFrame()

        dates_list = [
            "created_date",
            "last_updated_date",
            "agreed_payment_date",
            "agreed_delivery_date",
        ]
        for date in dates_list:
            fact_sales_order_df[date] = pd.to_datetime(fact_sales_order_df[date])

        dates = pd.melt(fact_sales_order_df, value_vars=dates_list, value_name="date")
        dim_date["date_id"] = dates[["date"]].drop_duplicates().reset_index(drop=True)

        dim_date["year"] = dim_date["date_id"].dt.year.astype("int64")
        dim_date["month"] = dim_date["date_id"].dt.month.astype("int64")
        dim_date["day"] = dim_date["date_id"].dt.day.astype("int64")
        dim_date["day_of_week"] = dim_date["date_id"].dt.dayofweek.astype("int64")
        dim_date["day_name"] = dim_date["date_id"].dt.day_name()
        dim_date["month_name"] = dim_date["date_id"].dt.month_name()
        dim_date["quarter"] = dim_date["date_id"].dt.quarter.astype("int64")

        return dim_date

    except Exception as e:
        print(e)


def transform_currency(currency_df):
    """
    This function uses get_currency_by_code library in order to get a currency name by its international
    code, in order to test it we compared 2 pandas dataframes.
    This function removes unneeded columns.

    ARGS: currency dataframe:original data

    RETURNS: transformed dataframe"""
    if currency_df.empty:
        print("transform_currency - The input dataframe is empty.")
        return pd.DataFrame(columns=["currency_id", "currency_code", "currency_name"])

    try:
        dim_currency = currency_df.copy()
        currency_codes = list(dim_currency["currency_code"])
        dim_currency["currency_name"] = [
            get_currency_by_code(code).name for code in currency_codes
        ]
        return dim_currency[["currency_id", "currency_code", "currency_name"]]
    except Exception as e:
        print(e)


def transform_location(address_df):
    """
    This function changes the name of the first column of any given dataframe.

    ARGS:address dataframe

    RETURN: modified and reduced dataframe
    """
    if address_df.empty:
        print("transform_location - The input dataframe is empty.")
        return pd.DataFrame(
            columns=[
                "location_id",
                "address_line_1",
                "address_line_2",
                "district",
                "city",
                "postal_code",
                "country",
                "phone",
            ]
        )

    try:
        dim_location = address_df.copy()
        dim_location = dim_location.rename(columns={"address_id": "location_id"})
        return dim_location[
            [
                "location_id",
                "address_line_1",
                "address_line_2",
                "district",
                "city",
                "postal_code",
                "country",
                "phone",
            ]
        ]
    except Exception as e:
        print(e)
