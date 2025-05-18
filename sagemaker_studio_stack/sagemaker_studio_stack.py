from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_sagemaker as sagemaker,
)
from constructs import Construct

class SageMakerStudioStack(Stack):
    def __init__(self, scope: Construct, id: str, vpc_id: str, subnet_ids: list, domain_name: str, sagemaker_users: list, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create IAM Role for SageMaker Studio
        self.sagemaker_studio_role = iam.Role(self, "SageMakerStudioRole",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ]
        )

        # Create SageMaker Domain
        domain = sagemaker.CfnDomain(self, "SageMakerDomain",
            auth_mode="IAM",
            default_user_settings=sagemaker.CfnDomain.UserSettingsProperty(
                execution_role=self.sagemaker_studio_role.role_arn,
            ),
            domain_name=domain_name,
            subnet_ids=subnet_ids,
            vpc_id=vpc_id,
        )

        # Create User Profiles dynamically based on the config list
        for user_name in sagemaker_users:
            sagemaker.CfnUserProfile(self, f"SageMakerUserProfile-{user_name}",
                domain_id=domain.attr_domain_id,
                user_profile_name=user_name,
            )
