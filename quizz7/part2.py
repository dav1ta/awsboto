import boto3
import datetime


ec2_client = boto3.client('ec2', region_name='us-east-1')


def list_snapshots():
    response = ec2_client.describe_snapshots(OwnerIds=['self'])
    volumes = response.get('Snapshots')

    return volumes


def delete_snapshot_older_than_week(snapshot_id):
    ec2_client.delete_snapshot(
        SnapshotId=snapshot_id
    )


def list_and_delete_snapshots():
    snapshots = list_snapshots()
    print(snapshots)
    for snap in snapshots:
        delta = datetime.datetime.now(
        ) - snap['StartTime'].replace(tzinfo=None)
        if delta.days > 7:
            delete_snapshot_older_than_week(snap['SnapshotId'])


if __name__ == '__main__':
    list_and_delete_snapshots()
