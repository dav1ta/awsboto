import boto3
import argparse


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db')
    return parser.parse_args()


def create_db_snapshot(client, db_identifier):
    client.create_db_snapshot(
        DBInstanceIdentifier=db_identifier,
        DBSnapshotIdentifier=f'Snap{db_identifier}',
        Tags=[
            {
                'Key': 'Name',
                'Value': f'Snapshot{db_identifier}'
            },
        ]
    )
    print('snapshot created')


def main():
    parser = init_argparse()
    client = boto3.client('rds', region_name='us-east-1')
    create_db_snapshot(client, parser.db)


if __name__ == '__main__':
    main()
