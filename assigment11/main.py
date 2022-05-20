import boto3
import urllib


def create_instance(client, group_id, subnet_id):
    response = client.run_instances(
        BlockDeviceMappings=[{'DeviceName': '/dev/sdh',
                              'Ebs': {'DeleteOnTermination': True,
                                      'VolumeSize': 10,
                                      'VolumeType': 'gp2',
                                      'Encrypted': False}
                              }],
        ImageId='ami-0022f774911c1d690',
        InstanceType='t2.micro',
        KeyName='davit-key',
        InstanceInitiatedShutdownBehavior='terminate',
        MaxCount=1,
        MinCount=1,
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
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
    )
    key_id = response.get('KeyPairId')
    with open(f'{key_name}.pem', 'w') as file:
        file.write(response.get('KeyMaterial'))
    print('Key pair id - ', key_id)
    return key_id


def create_security_group(client, name, description, vpc_id):
    response = client.create_security_group(
        Description=description,
        GroupName=name,
        VpcId=vpc_id)
    group_id = response.get('GroupId')

    print('Security Group Id - ', group_id)

    return group_id


def add_ssh_access_sg(client, sg_id, ip_address):
    ip_address = f'{ip_address}/32'

    response = client.authorize_security_group_ingress(
        CidrIp=ip_address,
        FromPort=22,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=22,
    )
    if response.get('Return'):
        print('Rule added successfully')
    else:
        print('Rule was not added')


def get_my_public_ip():
    external_ip = urllib.request.urlopen(
        'https://ident.me').read().decode('utf8')
    print('Public ip - ', external_ip)

    return external_ip


def add_http_access_sg(client, sg_id):
    ip_address = '0.0.0.0/0'

    response = client.authorize_security_group_ingress(
        CidrIp=ip_address,
        FromPort=80,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=80,
    )
    if response.get('Return'):
        print('Rule added successfully')
    else:
        print('Rule was not added')


def main():
    vpc_id = 'vpc-034ad50c0d0387a10'
    subnet_id = 'subnet-03f52d2d2f75f8ea9'
    client = boto3.client('ec2', region_name='us-east-1')
    # create_key_pair(client,"davit-key")
    group_id = create_security_group(client, 'chemi', 'ragaca', vpc_id)
    add_http_access_sg(client, group_id)
    my_ip = get_my_public_ip()
    add_ssh_access_sg(client, group_id, my_ip)
    create_instance(client, group_id, subnet_id)


if __name__ == '__main__':
    main()
