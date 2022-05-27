import boto3
import json

TABLE_NAME = 'datochantu'

dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)
response = table.scan()
data = response['Items']


with open('data.json', 'w') as f:
    f.write(json.dumps(data))
