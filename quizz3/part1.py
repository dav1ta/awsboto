import boto3
import argparse


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vpc')
    parser.add_argument('-s', '--subnet')
    parser.add_argument('-g', '--vpc')
    return parser.parse_args()


def create_instance(client, group_id, subnet_id):
    response = client.run_instances(
        BlockDeviceMappings=[{'DeviceName': '/dev/sdh',
                              'Ebs': {'DeleteOnTermination': True,
                                      'VolumeSize': 8,  # < volume 8
                                      'VolumeType': 'gp2',
                                      'Encrypted': False}
                              }],
        ImageId='ami-0022f774911c1d690',
        InstanceType='t2.micro',  # t2 mitro
        KeyName='my-quiz-key-1',
        InstanceINetworkInterfacestiatedShutdownBehavior='terminate',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': False,  # not public ip
                'DeleteOnTermination': True,
                'Description': 'string',
                'Groups': [
                    group_id
                ],
                'DeviceIndex':0,
                'SubnetId':subnet_id
            },
        ])

    for instance in response.get('Instances'):
        instance_id = instance.get('InstanceId')
        print('InstanceId - ', instance_id)


def create_key_pair(client, key_name):
    response = client.create_key_pair(
        KeyName=key_name,
        KeyType='rsa',
        KeyFormat='pem',    # api call says it has not parameter
                            # KeyFormat and without it works,
                            # i still add here as docs says.
    )
    key_id = response.get('KeyPairId')
    with open(f'{key_name}.pem', 'w') as file:
        file.write(response.get('KeyMaterial'))
    print('Key pair id - ', key_id)
    return key_id


def main():
    parser = init_argparse()
    client = boto3.client('ec2', region_name='us-east-1')
    create_key_pair(client, 'my-quiz-key-1')
    create_instance(client, parser.group, parser.subnet)


if __name__ == '__main__':
    main()
