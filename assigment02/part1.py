import argparse
import boto3

"""დაწერეთ პროგრამა, რომელსაც არგუმენტად გადაეცემა ბაკეტის სახელი.
პროგრამამ უნდა შეამოწმოს ბაკეტი არსებობს თუ არა. თუ არსებობს უნდა
დაწეროს რომ ბაკეტი უკვე არსებობს, თუ არ არსებობს უნდა შექმნას ის."""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    return parser.parse_args()


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
    if response['HTTPStatusCode'] == 200:
        print(f"Bucket Created Success at {response['date']}")
    print(response)


if __name__ == '__main__':
    parser = init_argparse()
    print(parser)
    if not parser.name:
        raise SystemExit('Please Specify a bucket name using --name argument')

    s3_client = boto3.client('s3')
    if not check_bucket_by_name(s3_client, parser.name):
        create_bucket_by_name(s3_client, parser.name)
