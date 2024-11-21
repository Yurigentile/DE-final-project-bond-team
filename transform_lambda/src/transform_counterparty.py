import pandas as pd

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
    """
    dim_counterparty = counterparty_df.copy()
    dim_counterparty = dim_counterparty.merge(
        address_df, how="left",
                    left_on="legal_address_id",
                    right_on="address_id"
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

