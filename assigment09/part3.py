import boto3
import argparse


'''
დაწერეთ პროგრამა რომელსაც არგუმენტად გადაეცემა VPC იდენტიფიკატორი.
პროგრამამ უნდა შექმნას ინტერნეტ გეითვეი(IGW) და მიაბას VPC-ს. პროგრამამ
ეკრანზე უნდა დაბეჭდოს შექმნილი IGW-ს იდენტიფიკატორი.
'''


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vpc')
    return parser.parse_args()


def create_and_attach_igw(client, vpc_id):
    response = client.create_internet_gateway()
    igw_id = response.get('InternetGateway').get('InternetGatewayId')
    response = client.attach_internet_gateway(
        VpcId=vpc_id,
        InternetGatewayId=igw_id
    )
    print(igw_id)
    return(igw_id)


def main():
    parser = init_argparse()
    client = boto3.client('ec2', region_name='us-east-1')
    create_and_attach_igw(client, parser.vpc)


if __name__ == '__main__':
    main()
