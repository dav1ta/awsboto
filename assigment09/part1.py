import boto3
import argparse

"""
1. დაწერეთ პროგრამა რომელიც შექმნის VPC-ს CIDR ბლოკით 10.10.0.0/16. VPC
დაადეთ ორი თაგი(tag) გასაღებებით Name და Creator. Name თაგში ჩაწერეთ რაც
გინდათ, ხოლო Creator თაგში ჩაწერეთ თქვენი სახელი. პროგრამამ ეკრანზე უნდა
დაბეჭდოს შექმნილი VPC-ის იდენტიფიკატორი.
"""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    return parser.parse_args()


def add_name_to_resource(client, resource_id, key, value):
    client.create_tags(
        Resources=[resource_id],
        Tags=[
            {
                'Key': key,
                'Value': value
            }
        ]
    )


def create_vpc(client):
    response = client.create_vpc(CidrBlock='10.10.0.0/16')
    vpc_id = response.get('Vpc').get('VpcId')
    waiter = client.get_waiter('vpc_available')
    waiter.wait(VpcIds=[vpc_id])
    add_name_to_resource(client, vpc_id, 'Name', 'MyVpc')
    add_name_to_resource(client, vpc_id, 'Creator', 'Daviti')
    print(vpc_id)
    return(vpc_id)


def main():
    client = boto3.client('ec2', region_name='us-east-1')

    create_vpc(client)


if __name__ == '__main__':
    main()
