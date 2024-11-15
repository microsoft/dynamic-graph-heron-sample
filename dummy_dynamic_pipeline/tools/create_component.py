# Import required libraries
import os
# enable private features
os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"] = "True"
print(os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"])

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from dynamic_subgraph import dynamic_subgraph


if __name__ == "__main__":
    credential = DefaultAzureCredential()
    ml_client =  MLClient.from_config(credential=credential)
    # dynamic_subgraph_func = ml_client.components.get(name="dynamic_subgraph", version="2024-11-13-02-33-08-6203985")
    dynamic_subgraph_func = ml_client.components.create_or_update(dynamic_subgraph, version="10")
