import boto3
import argparse


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rds')

    return parser.parse_args()


def increase_db_memory(client, db_ident, memory):
    client.modify_db_instance(
        DBInstanceIdentifier=db_ident,
        AllocatedStorage=memory,
    )


def increase_db_memory_by_perc(client, db_ident, percentage):

    response = client.describe_db_instances(
        DBInstanceIdentifier=db_ident,
    )
    print(response)
    memory = response['DBInstances'][0]['AllocatedStorage']
    increased_memory = int(memory)+int(memory)*percentage//100

    increase_db_memory(client, db_ident, increased_memory)


def main():
    parser = init_argparse()
    client = boto3.client('rds', region_name='us-east-1')
    increase_db_memory_by_perc(client, parser.rds, 25)


if __name__ == '__main__':
    main()
