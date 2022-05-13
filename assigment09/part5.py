import boto3
import argparse

"""
დაწერეთ პროგრამა რომელსაც არგუმენტად გადაეცემა სამარშუტო
ცხრილი(Routing table)-ის იდენტიფიკატორი და ინტერნეტ გეითვეის
იდენტიფიკატორი. პროგრამამ უნდა ჩაამატოს გზა სამარშუტო ცხრილში ინტერნეტ
გეითვეიმდე.
"""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--route')
    parser.add_argument('-i', '--igtw')
    return parser.parse_args()


def attach_igw_to_route_table(client, igw_id, rtb_id):
    client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id,
        RouteTableId=rtb_id,
    )
    print('added')


def main():
    parser = init_argparse()
    client = boto3.client('ec2', region_name='us-east-1')
    attach_igw_to_route_table(client, parser.igtw, parser.route)


if __name__ == '__main__':
    main()
