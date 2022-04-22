import io
import json
from pprint import pprint
from urllib.request import urlopen, Request

import boto3

API_TOKEN = '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'

headers = {'Authorization': f'Bearer {API_TOKEN}'}
API_URL = 'https://api-inference.huggingface.co/models/facebook/detr-resnet-50'

s3_client = boto3.client('s3')


def query_image(f):
    http_request = Request(API_URL, data=f.read(), headers=headers)
    with urlopen(http_request) as response:
        result = response.read().decode()
        print(result)
    return result


def lambda_handler(event, _):
    pprint(event)
    for record in event.get('Records'):
        bucket = record.get('s3').get('bucket').get('name')
        key = record.get('s3').get('object').get('key')

        print('Bucket', bucket)
        print('Key', key)

        # Download file from bucket
        file = io.BytesIO()
        s3_client.download_fileobj(Bucket=bucket, Key=key, Fileobj=file)
        file.seek(0)

        # Send file to Huggingface API
        result = query_image(file)
        print('result', result)

        # Upload result to bucket as json
        result_key = key.replace('.jpeg', '.json')
        file = io.BytesIO()
        file.write(result.encode('utf-8'))
        file.seek(0)

        s3_client.upload_fileobj(file, bucket, result_key)

    return {'statusCode': 200, 'body': json.dumps('Done!')}
