from aws_cdk import App
from aws_cdk.assertions import Template
from sagemaker_studio_stack.sagemaker_studio_stack import SageMakerStudioStack

def test_sagemaker_studio_domain_and_users():
    app = App()  # <-- Fix here: use App(), not Stack.App()
    
    vpc_id = "vpc-123456"
    subnet_ids = ["subnet-123", "subnet-456"]
    domain_name = "studio-domain"
    users = ["alice", "bob"]

    stack = SageMakerStudioStack(
        app,
        "TestStudioStack",
        vpc_id=vpc_id,
        subnet_ids=subnet_ids,
        domain_name=domain_name,
        sagemaker_users=users
    )
    template = Template.from_stack(stack)

    template.has_resource_properties("AWS::SageMaker::Domain", {
        "AuthMode": "IAM",
        "DomainName": domain_name,
        "SubnetIds": subnet_ids,
        "VpcId": vpc_id
    })

    for user in users:
        template.has_resource_properties("AWS::SageMaker::UserProfile", {
            "UserProfileName": user
        })
