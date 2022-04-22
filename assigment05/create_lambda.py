import boto3
import io
import zipfile


def create_zip(file_name):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zipped:
        zipped.write(file_name)
    buffer.seek(0)
    return buffer.read()


def get_role_arn(client, role_name):
    return client.get_role(RoleName=role_name)['Role']['Arn']


def create_lambda(client, function_name, role, handler, function_file):

    client.create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role=role,
        Handler=f"{function_file.split('.')[0]}.{handler}",
        Code={'ZipFile': create_zip(function_file)},
    )


def main():
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    iam_client = boto3.client('iam')
    iam_role = get_role_arn(iam_client, 'LabRole')
    function_file_name = 'lambda_func.py'
    print(iam_role)
    create_lambda(
        lambda_client, 'imagesrocessor',
        iam_role, 'lambda_handler', function_file_name
    )


if __name__ == '__main__':
    main()
