from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct
from typing import List, Optional


class AwsVpcStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        create_new_vpc: bool,
        existing_vpc_id: Optional[str] = None,
        existing_subnet_ids: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        if create_new_vpc:
            # Create VPC with 1 NAT Gateway and 3 subnets (1 public + 2 private)
            self.vpc = ec2.Vpc(self, "CustomVpc",
                cidr="10.0.0.0/16",
                max_azs=2,
                nat_gateways=1,
                subnet_configuration=[
                    ec2.SubnetConfiguration(
                        name="PublicSubnet",
                        subnet_type=ec2.SubnetType.PUBLIC,
                        cidr_mask=24
                    ),
                    ec2.SubnetConfiguration(
                        name="PrivateSubnet",
                        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                        cidr_mask=24
                    ),
                ]
            )

            # Pick private subnets
            self.subnet_ids = [
                subnet.subnet_id
                for subnet in self.vpc.select_subnets(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
                ).subnets
            ]
        else:
            if not existing_vpc_id or not existing_subnet_ids:
                raise ValueError("Must provide existing_vpc_id and existing_subnet_ids when create_new_vpc is False")

            self.vpc = ec2.Vpc.from_lookup(self, "ExistingVpc", vpc_id=existing_vpc_id)
            self.subnet_ids = existing_subnet_ids
