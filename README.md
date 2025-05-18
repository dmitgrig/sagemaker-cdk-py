# SageMaker CDK Python Project

This project uses AWS CDK in Python to provision and manage Amazon SageMaker resources including SageMaker Models and SageMaker Studio environments. It provides infrastructure-as-code stacks to deploy machine learning models and SageMaker Studio domains with user profiles.

---

## Project Structure

- `sagemaker_model_stack/`  
  CDK stack defining SageMaker Model resources and endpoints.

- `sagemaker_studio_stack/`  
  CDK stack defining SageMaker Studio Domain and User Profiles.

- `tests/unit/`  
  Unit tests validating the CDK stacks using AWS CDK assertions.

---

## Prerequisites

- Python 3.12+
- AWS CLI configured with appropriate permissions
- AWS CDK Toolkit installed (`npm install -g aws-cdk`)
- Virtual environment tool (optional but recommended)

---

## Environment Variables

| Variable                     | Description                                         | Required | Example                          |
|------------------------------|-----------------------------------------------------|----------|---------------------------------|
| `AWS_REGION`                 | AWS region where resources will be deployed          | Yes      | `us-west-2`                     |
| `SAGEMAKER_ROLE_ARN`         | ARN of the IAM role used by SageMaker                 | Yes      | `arn:aws:iam::123456789012:role/SageMakerRole` |
| `CONTAINER_URI`              | URI of the Docker container image used for the model | Yes      | `123456789012.dkr.ecr.us-west-2.amazonaws.com/my-container:latest` |
| `VPC_ID`                    | ID of the VPC where SageMaker Studio is deployed     | No       | `vpc-123456`                    |
| `SUBNET_IDS`                | List of subnet IDs for SageMaker Studio               | No       | `subnet-123,subnet-456`        |
| `DOMAIN_NAME`               | Name of the SageMaker Studio domain                    | No       | `studio-domain`                 |
| `CONTAINER_CONFIG_FRAMEWORK`           | ML framework used in the container                  | Yes      | `huggingface`                   |
| `CONTAINER_CONFIG_VERSION`             | Version of the ML framework                         | Yes      | `4.26.0`                       |
| `CONTAINER_CONFIG_IMAGE_SCOPE`         | Scope of container image (training/inference)      | Yes      | `inference`                    |
| `CONTAINER_CONFIG_BASE_FRAMEWORK_VERSION` | Base ML framework version (e.g., PyTorch version) | Yes      | `pytorch1.13.1`                |
| `CONTAINER_CONFIG_INSTANCE_TYPE`       | SageMaker instance type for endpoint deployment    | Yes      | `ml.m5.large`                  |


*Note: Some parameters can also be passed programmatically when instantiating stacks instead of using environment variables.*

---

## Setup

1. Clone the repo and create a Python virtual environment:

   ```bash
   git clone <your-repo-url>
   cd sagemaker-cdk-py
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

2. Deployment

   ```bash
   cdk synth
   cdk deploy --all
   ```

3. Single stack deployment

   ```bash
   cdk synth
   cdk deploy AwsVpcStack
   ```


## Testing

   ```bash
   pytest tests/unit
   ```
   
   
## Decommision resources

   ```bash
   cdk destroy --all
   ```
   