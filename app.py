#!/usr/bin/env python3
import json
import aws_cdk as cdk
from sagemaker import image_uris

from aws_vpc_stack.aws_vpc_stack import AwsVpcStack
from sagemaker_studio_stack.sagemaker_studio_stack import SageMakerStudioStack
from sagemaker_model_stack.sagemaker_model_stack import SageMakerModelStack

# Load config from JSON file
with open("config.json") as f:
    config = json.load(f)

env = cdk.Environment(
    account=config["aws_account"],
    region=config["aws_region"]
)

app = cdk.App()

# Create VPC Stack
vpc_stack = AwsVpcStack(
    app,
    "AwsVpcStack",
    create_new_vpc=config["deploy_new_vpc"],
    existing_vpc_id=config.get("existing_vpc_id"),
    existing_subnet_ids=config.get("existing_subnet_ids", []),
    env=env
)

# Retrieve container URI from config parameters
container_uri = image_uris.retrieve(
    framework=config["container_config"]["framework"],
    region=config["aws_region"],
    version=config["container_config"]["version"],
    image_scope=config["container_config"]["image_scope"],
    base_framework_version=config["container_config"]["base_framework_version"],
    instance_type=config["container_config"]["instance_type"]
)

# Create SageMaker Studio Stack
studio_stack = SageMakerStudioStack(
    app,
    "SageMakerStudioStack",
    vpc_id=vpc_stack.vpc.vpc_id,
    subnet_ids=vpc_stack.subnet_ids,
    domain_name=config["domain_name"],
    sagemaker_users=config["sagemaker_users"],
    env=env
)

# Create SageMaker Model Stack, passing env_vars and instance_type from config
SageMakerModelStack(
    app,
    "SageMakerModelStack",
    sagemaker_role=studio_stack.sagemaker_studio_role,
    container_uri=container_uri,
    env_vars=config["container_config"].get("env_vars", {}),  # fallback to empty dict if missing
    instance_type=config["container_config"]["instance_type"],
    env=env
)

app.synth()
