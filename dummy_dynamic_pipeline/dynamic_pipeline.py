# Import required libraries
import os
# enable private features
os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"] = "True"
print(os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"])

import json
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import UserIdentityConfiguration
# from azure.ai.ml import PipelineJob
# pipeline_job: PipelineJob
# pipeline_job.settings._dataset_access_mode = "DatasetInDpv2"
from azure.ai.ml import Input, Output

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
ml_client =  MLClient.from_config(credential=credential)
consume_model_func = ml_client.components.get(name="consume_model")
gen_silos_func = ml_client.components.get(name="gen_silos")
dynamic_subgraph_func = ml_client.components.get(name="dynamic_subgraph")

# !!! Change below value for the default_compute_target to use your own compute cluster
@pipeline(default_compute_target="CWC-Cluster", display_name="dynamic_pipeline_with_registered_components")
def dynamic_parent_pipeline(silos: str, valid_data: Input):
    silos_node = gen_silos_func(params=silos)

    subgraph_node = dynamic_subgraph_func(
        input_silos=silos_node.outputs.output, valid_data=valid_data
    )
    # Note: this user identity is required to submit a dynamic run since we need create the dynamic run on behalf of the user
    subgraph_node.identity = UserIdentityConfiguration()

    consume_node = consume_model_func(
        model=subgraph_node.outputs.output_model,
        metric=subgraph_node.outputs.output_metric,
        condition=subgraph_node.outputs.condition_output,
    )

if __name__ == "__main__":
    dynamic_pipeline = dynamic_parent_pipeline(
        silos="silo1,silo2,silo3,silo4,silo5,silo6",
        valid_data=Input(
            path="wasbs://demo@dprepdata.blob.core.windows.net/Titanic.csv", type="uri_file"
        ),
    )

    ml_client.jobs.create_or_update(dynamic_pipeline, experiment_name="dynamic_pipeline")
