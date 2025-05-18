from aws_cdk import App, Stack
from aws_cdk.assertions import Template
from aws_cdk import aws_iam as iam
from sagemaker_model_stack.sagemaker_model_stack import SageMakerModelStack


def test_sagemaker_model_resources():
    app = App()
    # Create a separate stack for the role (to simulate your setup)
    role_stack = Stack(app, "TestRoleStack")

    role = iam.Role(
        role_stack,
        "TestRole",
        assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com")
    )

    # Create the SageMaker model stack, passing the role from the other stack
    sm_stack = SageMakerModelStack(
        app,
        "TestSageMakerModelStack",
        sagemaker_role=role,
        container_uri="123456789012.dkr.ecr.us-west-2.amazonaws.com/my-container:latest"
    )

    template = Template.from_stack(sm_stack)

    # Find all SageMaker Model resources
    models = [
        r for r in template.find_resources("AWS::SageMaker::Model").values()
        if r["Properties"].get("ModelName") == "HuggingFaceModelUnique"
    ]
    assert len(models) == 1

    model_props = models[0]["Properties"]

    # Check that ExecutionRoleArn exists and is an object (because of cross-stack reference)
    assert "ExecutionRoleArn" in model_props
    assert isinstance(model_props["ExecutionRoleArn"], dict)

    # Check PrimaryContainer fields
    primary_container = model_props["PrimaryContainer"]
    assert primary_container["Image"] == "123456789012.dkr.ecr.us-west-2.amazonaws.com/my-container:latest"
    assert primary_container["Environment"] == {
        "HF_MODEL_ID": "distilbert-base-uncased-finetuned-sst-2-english",
        "HF_TASK": "text-classification"
    }

    # Other assertions for EndpointConfig and Endpoint (unchanged)
    template.has_resource_properties("AWS::SageMaker::EndpointConfig", {
        "ProductionVariants": [{
            "InstanceType": "ml.m5.large",
            "InitialInstanceCount": 1,
            "ModelName": "HuggingFaceModelUnique",
            "VariantName": "AllTraffic"
        }]
    })

    template.has_resource_properties("AWS::SageMaker::Endpoint", {
        "EndpointName": "huggingface-endpoint"
    })
