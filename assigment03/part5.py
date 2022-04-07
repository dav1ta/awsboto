import os
import argparse
import botocore
import boto3
from tempfile import NamedTemporaryFile


"""'დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი და
ფაილის სახელი. პროგრამამ უნდა ატვირთოს ფაილის ბოლოს წინა ვერსია ახალ
ვერსიად ბაკეტში"""


def init_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket')
    parser.add_argument('-f', '--file')
    return parser.parse_args()


def filter_versions(client, bucket_name: str, prefix: str) -> list[str]:
    resp = client.list_object_versions(Prefix=prefix, Bucket=bucket_name)
    return [d['VersionId'] for d in resp['Versions']]


def download_file(
    client, file_name: str, bucket_name: str, output: str, version_id: str
) -> bool:
    try:
        client.meta.client.download_file(
            bucket_name, file_name, output, ExtraArgs={'VersionId': version_id}
        )
        return True
    except botocore.exceptions.ClientError:
        return False


def upload_file(client, file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

        print(file_name)

    try:
        client.upload_file(file_name, bucket, object_name)
    except botocore.exceptions.ClientError as e:
        print(e)
        return False
    return True


def main() -> None:
    parser = init_argparse()
    if not parser.bucket or not parser.file:
        raise SystemExit(
            'Please Specify a bucket name using  arguments --file and --bucket'
        )
    s3 = boto3.client('s3')
    s3_res = boto3.resource('s3')
    versions = filter_versions(s3, parser.bucket, parser.file)
    prev_version = versions[1] if len(versions) >= 1 else None
    if not prev_version:
        raise SystemExit('No Previous version Found')

    temp_file = NamedTemporaryFile()
    download_file(s3_res, parser.file, parser.bucket,
                  temp_file.name, prev_version)
    print('file Downloaded')
    upload_file(s3, temp_file.name, parser.bucket, parser.file)
    print('file Uploaded')


if __name__ == '__main__':
    main()
