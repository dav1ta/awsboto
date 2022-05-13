from .part1 import create_vpc
from .part2 import create_subnet
from .part3 import create_and_attach_igw
from .part4 import create_routing_table
from .part5 import attach_igw_to_route_table
from .part6 import attach_subnet_to_routing_table
import boto3


def main():
    client = boto3.client('ec3', region='us-east-1')

    vpc = create_vpc(client)
    igw = create_and_attach_igw(client, vpc)
    subnet_id = create_subnet(client, vpc, '10.10.2.0/24')
    routing_table = create_routing_table(client)
    attach_igw_to_route_table(client, igw, routing_table)

    attach_subnet_to_routing_table(client, subnet_id, routing_table)

    # private

    subnet_id_private = create_subnet(client, vpc, '10.10.3.0/24')
    private_route = create_routing_table(client, vpc)
    attach_subnet_to_routing_table(client, subnet_id_private, private_route)


if __name__ == '__main__':
    main()
