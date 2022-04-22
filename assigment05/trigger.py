import boto3


def get_lambda_arn(client, function_name):
    return client.get_function(FunctionName=function_name)['Configuration'][
        'FunctionArn'
    ]


def add_trigger_s3(client, bucket, event_name, lambda_function_arn):
    client.put_bucket_notification_configuration(
        Bucket=bucket,
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [
                {
                    'Id': event_name,
                    'LambdaFunctionArn': lambda_function_arn,
                    'Events': [
                        's3:ObjectCreated:*',
                    ],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {'Name': 'suffix', 'Value': '.jpeg'},
                            ]
                        }
                    },
                },
            ],
        },
    )


def main():
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    function_arn = get_lambda_arn(lambda_client, 'imageprocessor')
    s3_client = boto3.client('s3')
    add_trigger_s3(s3_client, 'imageprocessorbucket11',
                   'festsfsdf', function_arn)


if __name__ == '__main__':
    main()
