import unittest
from unittest.mock import patch, Mock, MagicMock
import json
from transform_lambda.load_new_data import load_new_data, retrive_list_of_files
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime
from decimal import Decimal

class TestS3Functions(unittest.TestCase):

    @patch('boto3.client')
    def setUp(self, mock_boto_client):
        # Mock S3 client
        self.mock_s3 = Mock()
        mock_boto_client.return_value = self.mock_s3

        # Mock bucket data
        def mock_list_objects_v2(Bucket):
            if Bucket == 'test-bucket':
                return {
                    'Contents': [
                        {'Key': 'fake_file1.json'},
                        {'Key': 'fake_file2.json'},
                        {'Key': 'fake_file3.json'},
                    ]
                }
            return {}
        
        self.mock_s3.list_objects_v2.side_effect = mock_list_objects_v2

    @patch('boto3.client')
    def test_retrieve_list_of_s3_files_when_bucket_has_files(self, mock_boto_client):
        mock_boto_client.return_value = self.mock_s3

        bucket = 'test-bucket'
        result = retrive_list_of_files(bucket)
        self.assertEqual(result, ['fake_file1.json', 'fake_file2.json', 'fake_file3.json'])

    @patch('boto3.client')
    def test_retrieve_list_of_s3_files_bucket_empty(self, mock_boto_client):
        mock_boto_client.return_value = self.mock_s3

        bucket = 'empty-bucket'
        result = retrive_list_of_files(bucket)
        self.assertEqual(result, [])

    @patch('boto3.client')
    def test_retrieve_list_of_s3_files_bucket_no_credentials(self, mock_boto_client):
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        # Simulate NoCredentialsError
        mock_s3.list_objects_v2.side_effect = NoCredentialsError

        with self.assertRaises(NoCredentialsError):
            retrive_list_of_files('test-bucket')



class TestLoadNewDataWithoutMoto(unittest.TestCase):

    @patch("transform_lambda.load_new_data.boto3.client")  
    def test_load_new_data(self, mock_boto_client):

        dataset_stub = {
    'design': [
        {
            'design_id': 472,
            'created_at':  '2024-11-19T12:20:10.216000',
            'design_name': 'Concrete',
            'file_location': '/usr/share',
            'file_name': 'concrete-20241026-76vi.json'
        },
        {
            'design_id': 473,
            'design_name': 'Rubber',
            'file_location': '/Users', 
            'file_name': 'rubber-20240916-1hsu.json'
        }
    ],
    'sales_order': [
        {
            'sales_order_id': 11165,
            'design_id': 69,
            'staff_id': 18,
            'counterparty_id': 19,
            'units_sold': 12145,
            'currency_id': 3,
            'agreed_delivery_date': '2024-11-15',
            'agreed_payment_date': '2024-11-15',
            'agreed_delivery_location_id': 26
        },
        {
            'sales_order_id': 11166,
            'design_id': 398,
            'staff_id': 14,
            'counterparty_id': 20,
            'units_sold': 75609,
            'currency_id': 3,
            'agreed_delivery_date': '2024-11-15',
            'agreed_payment_date': '2024-11-20',
            'agreed_delivery_location_id': 7
        }
    ],
    'staff':[],
    "currency":[],
    "counterparty":[],
    "address":[],
    "department":[],
    "purchase_order":[],
    "payment_type":[],
    "payment":[],
    "transaction":[]
}
        
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        bucket_name = "test-bucket"
        timestamp = "2024-11-14 12:00:00"
        mock_file_list = [
            f"{timestamp}/design.json",
            f"{timestamp}/sales_order.json"
        ]

        mock_s3.list_objects_v2.return_value = {
            "Contents": [{"Key": key} for key in mock_file_list]
        }

        mock_s3.get_object.side_effect = lambda Bucket, Key: {
            "Body": MagicMock(read=lambda: json.dumps(dataset_stub[Key.split('/')[-1].split('.')[0]]).encode('utf-8'))
        }

        tables = ["design", "sales_order"]

        result = load_new_data(bucket_name, tables)

        self.assertEqual(result, dataset_stub)
        self.assertIn("design", result)
        self.assertIn("sales_order", result)

        mock_s3.list_objects_v2.assert_called_once_with(Bucket=bucket_name)
        for key in mock_file_list:
            mock_s3.get_object.assert_any_call(Bucket=bucket_name, Key=key)

if __name__ == "__main__":
    unittest.main()