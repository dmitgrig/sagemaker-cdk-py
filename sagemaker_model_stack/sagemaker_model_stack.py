from aws_cdk import (
    Stack,
    aws_sagemaker as sagemaker,
    aws_iam as iam,
)
from constructs import Construct

class SageMakerModelStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        sagemaker_role: iam.Role,
        container_uri: str,
        env_vars: dict,
        instance_type: str,
        **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Generete unique model name
        model_name = f"HuggingFaceModel-{self.node.addr[-8:]}"

        # Create the SageMaker Model
        model = sagemaker.CfnModel(self, "HuggingFaceModel",
            execution_role_arn=sagemaker_role.role_arn,
            primary_container=sagemaker.CfnModel.ContainerDefinitionProperty(
                image=container_uri,
                environment=env_vars
            ),
            model_name=model_name
        )

        # Create Endpoint Configuration referencing the model by name
        endpoint_config = sagemaker.CfnEndpointConfig(self, "EndpointConfig",
            production_variants=[sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                model_name=model_name,
                initial_instance_count=1,
                instance_type=instance_type,
                variant_name="AllTraffic"
            )]
        )

        endpoint_config.node.add_dependency(model)

        # Create Endpoint referencing the EndpointConfig
        endpoint = sagemaker.CfnEndpoint(self, "Endpoint",
            endpoint_config_name=endpoint_config.attr_endpoint_config_name,
            endpoint_name="huggingface-endpoint"
        )
