
def check_bucket_by_name(client, bucket_name):
    response = client.list_buckets()
    for bucket in response['Buckets']:
        if bucket['Name'] == bucket_name:
            print('Bucket Exists')
            return True
    print('Bucket Not Exists...')
    return False


def create_bucket_by_name(client, bucket_name):
    response = client.create_bucket(Bucket=bucket_name)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Bucket Created Success')
    print(response)


def check_or_create_bucket(client, bucket_name):

    created = check_bucket_by_name(client, bucket_name)
    if not created:
        create_bucket_by_name(client, bucket_name)
