from transform_lambda.src.transform_table_currency import transform_currency
import pandas as pd

def xtest_transform_table_with_single_currency():
    currency_df_input = pd.DataFrame([
    {
        "currency_id": 1,
        "currency_code": "GBP",
        "created_at": "2022-11-03 14:20:49.962",
        "last_updated": "2022-11-03 14:20:49.962"
    },
    {
        "currency_id": 2,
        "currency_code": "USD",
        "created_at": "2022-11-03 14:20:49.962",
        "last_updated": "2022-11-03 14:20:49.962"
    },
    {
        "currency_id": 3,
        "currency_code": "EUR",
        "created_at": "2022-11-03 14:20:49.962",
        "last_updated": "2022-11-03 14:20:49.962"
    }
   ])
    expected_df = pd.DataFrame([{
        "currency_id": 1,
        "currency_code": "GBP",
        "currency_name": "Pound Sterling"
    },
    {
        "currency_id": 2,
        "currency_code": "USD",
        "currency_name": "US Dollar"
    },
    {
        "currency_id": 3,
        "currency_code": "EUR",
        "currency_name": "Euro"
    }])

    transformed_df = transform_currency(currency_df_input)
    pd.testing.assert_frame_equal(transformed_df,expected_df)
