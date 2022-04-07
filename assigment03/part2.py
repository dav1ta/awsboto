import boto3
import argparse

"""დაწერეთ პროგრამა, რომელსაც არგუმენტებად გადაეცემა ბაკეტის სახელი და
ფაილის სახელი. პროგრამამ მითითებულ ბაკეტში უნდა წაშალოს გადმოცემული
ფაილი"""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket')
    parser.add_argument('-f', '--file')
    return parser.parse_args()


def delete_bucket(client, file_name, bucket):
    resp = client.delete_object(Bucket=bucket, Key=file_name)
    print(resp)
    if resp['ResponseMetadata']['HTTPStatusCode'] == 204:
        return True
    return False


def main():
    parser = init_argparse()
    if not parser.bucket or not parser.file:
        raise SystemExit(
            'Please Specify a bucket name using  arguments --file and --bucket'
        )

    s3 = boto3.client('s3')

    delete_status = delete_bucket(s3, parser.file, parser.bucket)
    if delete_status:
        print('file deleted Successfully')


if __name__ == '__main__':
    main()
