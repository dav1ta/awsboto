import boto3
import argparse


'''
დაწერეთ პროგრამა რომელსაც გადაეცემა VPC იდენტიფიკატორი და CIDR
ბლოკი. პროგრამამ CIDR ბლოკის გამოყენებით უნდა შექმნას ქვე-ქსელი VPC-ში.
პროგრამამ ეკრანზე უნდა დაბეჭდოს შექმნილი ქვე-ქსელის იდენტიფიკატორი.
'''


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vpc')
    return parser.parse_args()


def create_subnet(client, vpc_id, cidr_block):
    response = client.create_subnet(
        CidrBlock=cidr_block,
        VpcId=vpc_id
    )
    subnet_id = response.get('Subnet').get('SubnetId')
    print(subnet_id)
    return subnet_id


def main():
    parser = init_argparse()
    client = boto3.client('ec2', region_name='us-east-1')
    create_subnet(client, parser.vpc, '10.10.1.0/24')


if __name__ == '__main__':
    main()
