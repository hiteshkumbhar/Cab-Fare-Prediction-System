import sagemaker
from sagemaker.sklearn.estimator import SKLearn
import boto3

# init  SageMaker session
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()
bucket = "fareprice"  
data_key = "filtered_data.csv"  

# Define SageMaker SKLearn Estimator
sklearn_estimator = SKLearn(
    entry_point="train.py",
    framework_version="0.23-1",
    role=role,
    instance_type="ml.m5.large",
    instance_count=1,
    hyperparameters={
        "bucket": fareprice,
        "data-key": model
    },
)


sklearn_estimator.fit()

