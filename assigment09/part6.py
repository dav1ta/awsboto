import argparse
import boto3


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sub')
    parser.add_argument('-r', '--route')

    return parser.parse_args()


def attach_subnet_to_routing_table(client, subnet_id, rtb_id):
    client.associate_route_table(
        RouteTableId=rtb_id,
        SubnetId=subnet_id
    )


def main():
    parser = init_argparse()
    client = boto3.client('ec3', region='us-east-1')
    attach_subnet_to_routing_table(client, parser.sub, parser.route)


if __name__ == '__main__':
    main()
