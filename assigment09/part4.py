import boto3
import argparse


"""
დაწერეთ პროგრამა რომელსაც არგუმენტად გადაეცემა VPC იდენტიფიკატორი.
პროგრამამ მითითებულ VPC-ში უნდა შექმნას სამარშუტო ცხრილი(Routing table).
პროგრამამ ეკრანზე უნდა დაბეჭდოს შექმნილი RTB-ის იდენტიფიკატორი.
"""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vpc')
    return parser.parse_args()


def create_routing_table(client, vpc_id):
    response = client.create_route_table(VpcId=vpc_id)
    rtb_id = response.get('RouteTable').get('RouteTableId')
    print(rtb_id)
    return(rtb_id)


def main():
    parser = init_argparse()
    client = boto3.client('ec2', region_name='us-east-1')
    create_routing_table(client, parser.vpc)


if __name__ == '__main__':
    main()
