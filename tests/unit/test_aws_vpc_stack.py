from aws_cdk import App
from aws_cdk.assertions import Template
from aws_cdk import Stack
from aws_vpc_stack.aws_vpc_stack import AwsVpcStack


def test_vpc_created_with_subnets():
    app = App()
    test_stack = Stack(app, "BaseStack")
    stack = AwsVpcStack(test_stack, "TestVpcStack", create_new_vpc=True)
    template = Template.from_stack(stack)

    template.has_resource_properties("AWS::EC2::VPC", {
        "CidrBlock": "10.0.0.0/16"
    })

    template.resource_count_is("AWS::EC2::Subnet", 4)
