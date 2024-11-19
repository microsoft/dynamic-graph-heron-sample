# Import required libraries
import os
# enable private features
os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"] = "True"
print(os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"])

import json
from azure.ai.ml.dsl import pipeline
from azure.ai.ml import UserIdentityConfiguration
# from azure.ai.ml import PipelineJob
# pipeline_job: PipelineJob
# pipeline_job.settings._dataset_access_mode = "DatasetInDpv2"
from azure.ai.ml import Input, Output

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
# ml_client =  MLClient.from_config(credential=credential)
ml_client = MLClient(
    credential=credential,
    subscription_id="8e083f31-61f8-49c5-96a2-1366c4e338c6",
    resource_group_name="BizChat",
    workspace_name="CWC-WS"
)
dynamic_subgraph_pipeline = ml_client.components.get(name="dynamic_parent_pipeline")

if __name__ == "__main__":
    dynamic_pipeline = dynamic_subgraph_pipeline(
            silos="silo1,silo2,silo3,silo4,silo5,silo6",
            valid_data=Input(
                path="wasbs://demo@dprepdata.blob.core.windows.net/Titanic.csv", type="uri_file"
            ),
    )
    dynamic_pipeline.settings.default_compute = "CWC-Cluster"

    ml_client.jobs.create_or_update(dynamic_pipeline, experiment_name="dynamic_pipeline")
