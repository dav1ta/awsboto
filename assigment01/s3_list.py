import boto3

"""
1.მოაწყვეთ სამუშაო გარემო. დაწერეთ პითონის პროგრამა რომელიც გაჩვენებთ
თქვენი სისტემიდან ყველა s3 საცავს.
2. დაწერეთ პროგრამა რომელიც დაბეჭდავს თქვენი სისტემიდან ყველა s3 საცავს
რომლის სახელიც იწყება prod-ით.
"""


def list_buckets(client):
    response = client.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')


def list_buckets_by_name(client, name):
    response = client.list_buckets()
    print(f'Buckets name startswith {name}')
    for bucket in response['Buckets']:
        if bucket['Name'].startswith(name):
            print(f'  {bucket["Name"]}')


if __name__ == '__main__':
    s3 = boto3.client('s3')
    list_buckets(s3)
    list_buckets_by_name(s3, 'prod')
