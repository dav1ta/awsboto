import boto3
from create_lambda import get_role_arn, create_lambda
from trigger import get_lambda_arn, add_trigger_s3
from bucket_create import check_or_create_bucket
import json


def add_permission_to_s3(client, func_name, bucket_name):
    client.add_permission(
        FunctionName=func_name,
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}',
    )


def create_and_assign_lambda_to_s3(
    bucket_name, event_name, function_name, role, handler, function_file
):
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    s3_client = boto3.client('s3')
    iam_client = boto3.client('iam')

    iam_role = get_role_arn(iam_client, role)

    check_or_create_bucket(s3_client, bucket_name)
    try:
        create_lambda(lambda_client, function_name,
                      iam_role, handler, function_file)
        print(f'lambda function {function_name} created')
    except Exception as e:
        print('lambda Exist Continuing...', e)

    function_arn = get_lambda_arn(lambda_client, function_name)
    try:
        add_permission_to_s3(lambda_client, function_name, bucket_name)
    except Exception as e:
        print('permission exists', e)
    try:
        add_trigger_s3(s3_client, bucket_name, event_name, function_arn)
    except Exception as e:
        print('Error Maybe Exists', e)
    print(f'trigger {event_name} added')


def main():
    with open('config.json', 'r') as f:

        configs = json.loads(f.read())
        for config in configs:
            create_and_assign_lambda_to_s3(**config)


if __name__ == '__main__':
    main()
