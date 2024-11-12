import json
import boto3

s3_client = boto3.client('s3', region_name = 'eu-west-2')

def s3_save(data, bucket, key):
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        print(f"Saved to {bucket}/{key}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise