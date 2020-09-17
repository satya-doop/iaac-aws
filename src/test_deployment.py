from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.client_locator import EC2Client

def main():
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()
    print('vpc created' + str(vpc_response))

    # Add name tag to VPC
    vpc_name = 'Boto3-VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)
    print("Added" + vpc_name + "to" + vpc_id)

    # Add IGW
    igw_response = vpc.create_internet_gateway()
    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    # Creat a public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.10.1.0/24')
    public_subnet_id = public_subnet_response['Subnet']['SubnetId']
    print("Subnet created for " + vpc_id + ":" + str(public_subnet_response))
    # Add name tag to public subnet ID
    vpc.add_name_tag(public_subnet_id, 'Boto3-PublicSubnet')

    # Create public route table
    public_route_table_response = vpc.create_public_route_table(vpc_id)

    rtb_id = public_route_table_response['RouteTable']['RouteTableId']
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)

    # Associate Public Subnet with Route Table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)

    # Allow auto assign public IP address for subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)

    # Create private subnet
    private_subnet_response = vpc.create_subnet(vpc_id, '10.10.2.0/24')
    private_subnet_id = private_subnet_response['Subnet']['SubnetId']
    print("Create private subnet " + private_subnet_id + " for vpc " + vpc_id)

    # Add name tag to private subnet
    vpc.add_name_tag(private_subnet_id, 'Boto3-PrivateSubnet')

    # EC2 Instances
    ec2 = EC2(ec2_client)
    print("Creating EC2 instance.....")

    # Creating a key pair
    key_pair_name = 'Boto3-KeyPair'
    key_pair_response = ec2.create_key_pair(key_pair_name)

    print("Create Key Pair with name " + key_pair_name + " : " + str(key_pair_response))

    # Create a security group
    public_security_group_name = "Boto3-Public-SG"
    public_security_group_description = "Public SG for public subnet internet access"
    public_security_group_response = ec2.create_security_group(public_security_group_name, public_security_group_description, vpc_id)
    public_security_group_id = public_security_group_response['GroupId']

    # Add public access to security group
    ec2.add_inbound_rule_to_sg(public_security_group_id)
    print("Added public access rule group")




if __name__=='__main__':
    main()