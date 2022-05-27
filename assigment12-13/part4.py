import boto3

client = boto3.client('dynamodb', region_name='us-east-1')
response = client.list_tables(
    Limit=100
)
for name in response['TableNames']:
    print(name)
