import boto3
import argparse


"""
დაწერეთ პროგრამა, რომელსაც არგუმენტად გადაეცემა ბაკეტის სახელი.
პროგრამამ უნდა შეამოწმოს ბაკეტი არსებობს თუ არა. თუ არსებობს უნდა
წაშალოს, თუ არ არსებობს დაბეჭდოს რომ ბაკეტი არ არსებობს.
"""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    return parser.parse_args()


def bucket_exists(client, bucket_name):
    bucket = client.Bucket(bucket_name)
    return bucket.creation_date


def delete_bucket(client, bucket_name):
    response = client.delete_bucket(Bucket=bucket_name)
    if response['ResponseMetadata']['HTTPStatusCode'] == 204:
        print('Bucket Deleted Successfully')


if __name__ == '__main__':
    parser = init_argparse()
    s3 = boto3.client('s3')
    s3_r = boto3.resource('s3')
    if not parser.name:
        raise SystemExit('Please Specify a bucket name using --name argument')

    if bucket_exists(s3_r, parser.name):
        print('Bucket Exists, Deleting ...')
        delete_bucket(s3, parser.name)
    else:
        print('Bucket does not exists')
