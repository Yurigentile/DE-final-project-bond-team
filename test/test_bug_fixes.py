"""
Unit tests for fixed bugs in transform_star.py and load functions.
These tests verify the bug fixes for:
1. sales_record_id is now a column (not index)
2. Empty DataFrames return proper empty DataFrame (not None)
3. Load functions properly raise errors instead of silent pass
"""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from lambda_transform.src.transform_star import (
    transform_sales_order,
    transform_counterparty,
    transform_design,
    transform_staff,
    transform_date,
    transform_currency,
    transform_location,
)


class TestSalesRecordIdFix:
    """Tests to verify sales_record_id is now a column, not an index."""

    def test_sales_record_id_is_column(self):
        """Verify sales_record_id appears as a column in the output DataFrame."""
        input_df = pd.DataFrame(
            [
                {
                    "sales_order_id": 1,
                    "created_at": "2022-11-03T14:20:52.186",
                    "last_updated": "2022-11-03 14:20:52.186",
                    "design_id": 2,
                    "staff_id": 19,
                    "counterparty_id": 8,
                    "units_sold": 42972,
                    "unit_price": 3.94,
                    "currency_id": 2,
                    "agreed_delivery_date": "2022-11-07",
                    "agreed_payment_date": "2022-11-08",
                    "agreed_delivery_location_id": 8,
                }
            ]
        )

        result = transform_sales_order(input_df)

        assert "sales_record_id" in result.columns, "sales_record_id should be a column"
        assert (
            result["sales_record_id"].iloc[0] == 1
        ), "First record should have sales_record_id = 1"

    def test_sales_record_id_increments_correctly(self):
        """Verify sales_record_id increments correctly for multiple records."""
        input_df = pd.DataFrame(
            [
                {
                    "sales_order_id": 1,
                    "created_at": "2022-11-03T14:20:52.186",
                    "last_updated": "2022-11-03 14:20:52.186",
                    "design_id": 2,
                    "staff_id": 19,
                    "counterparty_id": 8,
                    "units_sold": 42972,
                    "unit_price": 3.94,
                    "currency_id": 2,
                    "agreed_delivery_date": "2022-11-07",
                    "agreed_payment_date": "2022-11-08",
                    "agreed_delivery_location_id": 8,
                },
                {
                    "sales_order_id": 2,
                    "created_at": "2022-11-03T14:20:52.188",
                    "last_updated": "2022-11-03 14:20:52.188",
                    "design_id": 3,
                    "staff_id": 10,
                    "counterparty_id": 4,
                    "units_sold": 65839,
                    "unit_price": 2.91,
                    "currency_id": 3,
                    "agreed_delivery_date": "2022-11-06",
                    "agreed_payment_date": "2022-11-07",
                    "agreed_delivery_location_id": 8,
                },
            ]
        )

        result = transform_sales_order(input_df)

        assert list(result["sales_record_id"]) == [
            1,
            2,
        ], "sales_record_id should be [1, 2]"

    def test_output_column_order(self):
        """Verify sales_record_id is the first column."""
        input_df = pd.DataFrame(
            [
                {
                    "sales_order_id": 1,
                    "created_at": "2022-11-03T14:20:52.186",
                    "last_updated": "2022-11-03 14:20:52.186",
                    "design_id": 2,
                    "staff_id": 19,
                    "counterparty_id": 8,
                    "units_sold": 42972,
                    "unit_price": 3.94,
                    "currency_id": 2,
                    "agreed_delivery_date": "2022-11-07",
                    "agreed_payment_date": "2022-11-08",
                    "agreed_delivery_location_id": 8,
                }
            ]
        )

        result = transform_sales_order(input_df)

        assert (
            result.columns[0] == "sales_record_id"
        ), "sales_record_id should be first column"


class TestEmptyDataFrameHandling:
    """Tests to verify empty DataFrames return proper empty DataFrame (not None)."""

    def test_transform_sales_order_empty_returns_dataframe(self):
        """Verify empty input returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame()
        result = transform_sales_order(empty_df)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"
        assert "sales_record_id" in result.columns, "Should have correct columns"
        assert "sales_order_id" in result.columns, "Should have correct columns"

    def test_transform_counterparty_empty_returns_dataframe(self):
        """Verify empty input returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame()
        result = transform_counterparty(empty_df, empty_df)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"
        assert "counterparty_id" in result.columns, "Should have correct columns"

    def test_transform_design_empty_returns_dataframe(self):
        """Verify empty input returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame()
        result = transform_design(empty_df)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"
        assert "design_id" in result.columns, "Should have correct columns"

    def test_transform_staff_empty_returns_dataframe(self):
        """Verify empty input returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame()
        result = transform_staff(empty_df, empty_df)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"
        assert "staff_id" in result.columns, "Should have correct columns"

    def test_transform_date_empty_returns_dataframe(self):
        """Verify empty input returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame()
        result = transform_date(empty_df)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"
        assert "date_id" in result.columns, "Should have correct columns"

    def test_transform_date_none_returns_dataframe(self):
        """Verify None input returns empty DataFrame with correct columns."""
        result = transform_date(None)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"

    def test_transform_currency_empty_returns_dataframe(self):
        """Verify empty input returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame()
        result = transform_currency(empty_df)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"
        assert "currency_id" in result.columns, "Should have correct columns"

    def test_transform_location_empty_returns_dataframe(self):
        """Verify empty input returns empty DataFrame with correct columns."""
        empty_df = pd.DataFrame()
        result = transform_location(empty_df)

        assert isinstance(result, pd.DataFrame), "Should return DataFrame, not None"
        assert len(result) == 0, "Should be empty"
        assert "location_id" in result.columns, "Should have correct columns"


class TestLoadParquetDataErrorHandling:
    """Tests to verify load_parquet_data properly raises errors."""

    @patch("lambda_load.src.load_parquet_data.retrive_list_of_files")
    def test_empty_bucket_returns_empty_dict(self, mock_retrieve):
        """Verify empty bucket returns empty dict instead of crashing."""
        from lambda_load.src.load_parquet_data import read_parquet_data_to_dataframe

        mock_retrieve.return_value = []

        result = read_parquet_data_to_dataframe("test-bucket")

        assert result == {}, "Should return empty dict for empty bucket"

    @patch("lambda_load.src.load_parquet_data.retrive_list_of_files")
    def test_invalid_timestamp_raises_error(self, mock_retrieve):
        """Verify invalid S3 key format raises ValueError."""
        from lambda_load.src.load_parquet_data import read_parquet_data_to_dataframe

        mock_retrieve.return_value = ["invalid_key_format.parquet"]

        with pytest.raises(ValueError, match="Invalid S3 key format"):
            read_parquet_data_to_dataframe("test-bucket")

    @patch("lambda_load.src.load_parquet_data.retrive_list_of_files")
    @patch("lambda_load.src.load_parquet_data.wr")
    def test_all_parquet_files_fail_raises_error(self, mock_wr, mock_retrieve):
        """Verify that if ALL parquet files fail to load, a RuntimeError is raised."""
        from lambda_load.src.load_parquet_data import read_parquet_data_to_dataframe

        mock_retrieve.return_value = ["2024-11-19 14:30/test.parquet"]
        mock_wr.s3.read_parquet.side_effect = Exception("S3 read failed")

        with pytest.raises(RuntimeError, match="Failed to load any parquet files"):
            read_parquet_data_to_dataframe("test-bucket")


class TestWarehouseLoadFunctions:
    """Tests for pg8000 warehouse load functions."""

    def test_default_schema_is_public(self):
        """Verify default schema is 'public' not 'project_team_6'."""
        from lambda_load.src.warehouse_load_functions_pg8000 import (
            load_data_into_warehouse,
        )
        import inspect

        sig = inspect.signature(load_data_into_warehouse)
        default_schema = sig.parameters["schema"].default

        assert (
            default_schema == "public"
        ), f"Default schema should be 'public', got '{default_schema}'"

    @patch("lambda_load.src.warehouse_load_functions_pg8000.boto3.client")
    def test_get_secret_returns_none_on_failure(self, mock_boto):
        """Verify get_secret returns None when secret not found."""
        from lambda_load.src.warehouse_load_functions_pg8000 import get_secret
        from botocore.exceptions import ClientError

        mock_client = MagicMock()
        mock_boto.return_value = mock_client
        mock_client.get_secret_value.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "Not found"}},
            "GetSecretValue",
        )

        result = get_secret("non-existent-secret")

        assert result is None, "Should return None for non-existent secret"
