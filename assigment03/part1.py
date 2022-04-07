import os
import boto3
import argparse
from botocore.exceptions import ClientError


"""
დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი და
ფაილის სახელი. პროგრამამ მითითებულ ბაკეტში უნდა ატვირთოს გადმოცემული
ფაილი.
"""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket')
    parser.add_argument('-f', '--file')
    return parser.parse_args()


def upload_file(client, file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print(e)
        return False
    return True


def main():

    parser = init_argparse()
    if not parser.bucket or not parser.file:
        raise SystemExit(
            'Please Specify a bucket name using  arguments --file and --bucket'
        )

    s3_client = boto3.client('s3')
    uploaded = upload_file(s3_client, parser.file, parser.bucket)
    if uploaded:
        print(
            f'file {parser.file} Successfully uploaded to bucket {parser.bucket}')


if __name__ == '__main__':
    main()
