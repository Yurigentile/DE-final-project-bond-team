import pandas as pd
from transform_lambda.src.transform_star_a import transform_staff, transform_date

def test_staff_success():
    df_staff = pd.DataFrame({
        'staff_id': [1],
        'first_name': ['A1'],
        'last_name': ['B0'],
        'department_id': [1],
        'extra_info': ['A1'],
        'email_address': ['B0']
    })

    df_department = pd.DataFrame({
        'department_id': [1],
        'department_name': ['C2'],
        'location': ['D2'],
        'extra_info_2': ['A2']
    })

    output = pd.DataFrame({
        'staff_id': [1],
        'first_name': ['A1'],
        'last_name': ['B0'],
        'department_name': ['C2'],
        'location': ['D2'],
        'email_address': ['B0']
    })

    pd.testing.assert_frame_equal(transform_staff(df_staff, df_department), output)


def test_date_success():
    df = pd.DataFrame({
        'created_date': ['2023-11-08'],
        'last_updated_date': ['2024-10-06'],
        'agreed_payment_date': ['2023-11-08'],
        'agreed_delivery_date': ['2023-09-07']
    })
    output = pd.DataFrame({
        'date_id': pd.to_datetime(['2023-11-8', '2024-10-06','2023-09-07']),
        'year': [2023, 2024, 2023],
        'month': [11, 10, 9],
        'day': [8, 6, 7],
        'day_of_week': [2, 6, 3], #3 if without 0-indexing
        'day_name': ['Wednesday', 'Sunday', 'Thursday'],
        'month_name': ['November', 'October', 'September'],
        'quarter': [4, 4, 3]
    })

    pd.testing.assert_frame_equal(transform_date(df), output)