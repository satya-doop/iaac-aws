class EC2:
    def __init__(self, client):
        self._client = client
        """" :type : pyboto3.ec2 """

    def create_key_pair(self, key_name):
        print("Creating Key_pair")
        return self._client.create_key_pair(
            KeyName=key_name
        )

    def create_security_group(self, group_name, description, vpc_id):
        print("Creating security group...")
        return self._client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )

    def add_inbound_rule_to_sg(self,security_group_id):
        print("Create inbound rule...")
        return self._client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )