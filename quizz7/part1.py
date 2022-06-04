
import boto3
import argparse


"""დაწერეთ პროგრამა რომელსაც გადაეცემა VPC იდენტიფიკატორი. პროგრამამ
უნდა შექმნას Security group. პროგრამამ უნდა შექმნას RDS ინსტანსი,
მეხსიერებით 60 GB, ძრავი mysql. RDS ინსტანსს განუსაზღვრეთ თქვენს მიერ
შექმნილი Security Group. პროგრამამ security group-ში უნდა გახსნას წვდომა
მონაცემთა ბაზის პორტისთვის ნებისმიერი IP მისამართიდან.(პროგრამა რომ
მორჩება მუშაობას შეამოწმეთ რომ შეგეძლოთ ბაზასთან დაკავშირება)"""


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vpc')
    return parser.parse_args()


def add_access_sg(client, sg_id, from_port, to_port, ip_address='0.0.0.0/0'):
    response = client.authorize_security_group_ingress(
        CidrIp=ip_address,
        FromPort=from_port,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=to_port,
    )
    if response.get('Return'):
        print('Rule added successfully')
    else:
        print('Rule was not added')


def create_rds_instance(client, engine, master_name, vpc_id):
    response = client.create_db_instance(
        DBName=master_name,
        DBInstanceIdentifier='demo-pg-db-2',
        AllocatedStorage=60,
        DBInstanceClass='db.t4g.micro',
        Engine=engine,
        MasterUsername=master_name,
        MasterUserPassword='strongrandompassword',
        VpcSecurityGroupIds=[
            vpc_id
        ],
        BackupRetentionPeriod=7,
        # Port=5432,
        MultiAZ=False,
        # EngineVersion='13.5',
        AutoMinorVersionUpgrade=True,
        # Iops=123, # Necessary when StorageType is 'io1'
        PubliclyAccessible=True,
        Tags=[{'Key': 'Name',   'Value': 'First RDS'}, ],
        StorageType='gp2',
        EnablePerformanceInsights=True,
        PerformanceInsightsRetentionPeriod=7,
        DeletionProtection=False,)
    _id = response.get('DBInstance').get('DBInstanceIdentifier')
    print(f'Instance {_id} was created')


def create_security_group(client, name, description, vpc_id):
    response = client.create_security_group(
        Description=description,
        GroupName=name,
        VpcId=vpc_id)
    group_id = response.get('GroupId')

    print('Security Group Id - ', group_id)

    return group_id


def main():
    parser = init_argparse()
    client = boto3.client('rds', region_name='us-east-1')
    ec2_client = boto3.client('ec2', region_name='us-east-1')
    sg = create_security_group(ec2_client, 'Saxeli', 'agwera', parser.vpc)
    add_access_sg(ec2_client, sg, 5432, 5432)
    create_rds_instance(client, 'postgres', 'postgre', sg)


if __name__ == '__main__':
    main()
