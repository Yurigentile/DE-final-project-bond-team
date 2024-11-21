import pandas as pd
from transform_lambda.src.transform_design import transform_design
from datetime import datetime
import pytest

def test_transform_design():
    input_df = pd.DataFrame([
        {
            "design_id": 472,
            "created_at": datetime(2024, 11, 14, 9, 41, 9, 839000),
            "design_name": "Concrete",
            "file_location": "/usr/share",
            "file_name": "concrete-20241026-76vi.json",
            "last_updated": datetime(2024, 11, 14, 9, 41, 9, 839000),
        },
        {
            "design_id": 473,
            "created_at": datetime(2024, 11, 15, 14, 9, 9, 608000),
            "design_name": "Rubber",
            "file_location": "/Users",
            "file_name": "rubber-20240916-1hsu.json",
            "last_updated": datetime(2024, 11, 15, 14, 9, 9, 608000),
        },
    ])
    
    expected_df = pd.DataFrame([
        {
            "design_id": 472,
            "design_name": "Concrete",
            "file_location": "/usr/share",
            "file_name": "concrete-20241026-76vi.json",
        },
        {
            "design_id": 473,
            "design_name": "Rubber",
            "file_location": "/Users",
            "file_name": "rubber-20240916-1hsu.json",
        },
    ])

    transformed_df = transform_design(input_df)
    pd.testing.assert_frame_equal(transformed_df, expected_df)
    
def test_transform_design_if_empty_df():
    input_df = pd.DataFrame()
    expected_df = pd.DataFrame()
    
    transformed_df = transform_design(input_df)
    pd.testing.assert_frame_equal(transformed_df, expected_df)

def test_transform_design_if_invalid_df_were_given():
    input_df = pd.DataFrame([
        {
            "invalid_column": 472,
            "invalid_column": 123
        }
    ])
    
    with pytest.raises(KeyError, match="Missing required columns"):
        transform_design(input_df)