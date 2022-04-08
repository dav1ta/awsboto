import boto3
import glob
import os
import json


def create_bucket_by_name(client, bucket_name):
    response = client.create_bucket(Bucket=bucket_name)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print('Bucket Created Success')


def upload_folder_to_bucket(client, directory_name, bucket_name):
    content_types = {'css': 'text/css', 'html': 'text/html'}
    directories = glob.glob(f'{directory_name}/**', recursive=True)
    for sub in directories:
        if os.path.isdir(sub):
            continue
        with open(sub, 'rb') as f:
            print('uploading ', sub)
            sub = sub.replace(f'{directory_name}/', '')
            file_bin = f.read()
            ext = sub.split('.')[-1]
            client.put_object(
                Bucket=bucket_name,
                Key=sub,
                Body=file_bin,
                ContentType=content_types[ext],
            )


def set_bucket_policy(client, bucket_name, bucket_policy):
    response = client.put_bucket_policy(
        Bucket=bucket_name, Policy=bucket_policy)
    if response['ResponseMetadata']['HTTPStatusCode'] == 204:
        print('Policy Saved Successfully')


def make_s3_web_host(client, bucket_name):
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }

    # Set the website configuration
    return client.put_bucket_website(
        Bucket=bucket_name, WebsiteConfiguration=website_configuration
    )


def get_website_url(client, bucket_name):
    response = client.head_bucket(Bucket=bucket_name)
    zone = response['ResponseMetadata']['HTTPHeaders'][
        'x-amz-bucket-region']
    return f'http://{bucket_name}.s3-website-{zone}.amazonaws.com'


def main():
    s3 = boto3.client('s3')
    bucket_name = 'datochanturia132243'
    root_dir = 'site'
    create_bucket_by_name(s3, bucket_name)
    upload_folder_to_bucket(s3, root_dir, bucket_name)
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
                        f'arn:aws:s3:::{bucket_name}/*',
                    ],
                }
            ],
        }
    )
    set_bucket_policy(s3, bucket_name, bucket_policy=bucket_policy)
    make_s3_web_host(s3, bucket_name)
    print('Website Hosted')
    print(get_website_url(s3, bucket_name))


if __name__ == '__main__':
    main()
