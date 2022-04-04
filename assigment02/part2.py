import boto3
import argparse
from botocore.exceptions import ClientError
import json

"""დაწერეთ პროგრამა, რომელსაც არგუმენტად გადაეცემა ბაკეტის სახელი.
პროგრამამ უნდა შეამოწმოს ბაკეტს გააჩნია თუ არა policy. თუ policy უკვე
არსებობს უნდა დაბეჭდოს რომ policy უკვე არსებოს, წინააღმდეგ შემთხვევაში,
უნდა შექმნას policy, რომელიც საჯაროდ წვდომადს გახდის ყველა ფაილს /dev და
/test პრეფიქსების ქვეშ."""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    return parser.parse_args()


def is_bucket_policy_created(client, name):
    try:
        response = client.get_bucket_policy(Bucket=name)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('Policy Exists')
            return True
    except ClientError:
        print('Bucket Policy Does not Exist')
        return False


def set_bucket_policy(client, bucket_name, bucket_policy):
    response = client.put_bucket_policy(Bucket=bucket_name,
                                        Policy=bucket_policy)
    if response['ResponseMetadata']['HTTPStatusCode'] == 204:
        print('Policy Saved Successfully')


if __name__ == '__main__':
    s3 = boto3.client('s3')
    parser = init_argparse()
    if not parser.name:
        raise SystemExit('Please Specify a bucket name using --name argument')

    bucket_policy = json.dumps(
        {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'AddPerm',
                    'Effect': 'Allow',
                    'Principal': '*',
                    'Action': ['s3:GetObject'],
                    'Resource': [
                        f'arn:aws:s3:::{parser.name}/dev/*',
                        f'arn:aws:s3:::{parser.name}/test/*',
                    ],
                }
            ],
        }
    )
    if not is_bucket_policy_created(s3, parser.name):
        set_bucket_policy(s3, parser.name, bucket_policy)
