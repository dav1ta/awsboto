import boto3
import argparse
from collections import Counter
from typing import Generator


def init_argparse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket')
    return parser.parse_args()


def list_all_files(client, bucket_name: str) -> Generator[str, None, None]:
    response = client.list_objects_v2(
        Bucket=bucket_name,
        Delimiter='string',
        MaxKeys=1000,
    )
    return (i['Key'] for i in response['Contents'])


def main() -> None:
    parser = init_argparse()
    s3 = boto3.client('s3')
    file_names = list_all_files(s3, parser.bucket)
    counter = Counter()
    for file_name in file_names:
        file_extenstion = file_name.split('.')[-1]
        counter[file_extenstion] += 1

    for ext, size in counter.items():
        print(f'{ext} - {size}')


if __name__ == '__main__':
    main()
