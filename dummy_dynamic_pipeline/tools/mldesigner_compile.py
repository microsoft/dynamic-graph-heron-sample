# Import required libraries
import os
# enable private features
os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"] = "True"
print(os.environ["AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED"])

import json
from mldesigner import compile

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from dynamic_subgraph import dynamic_subgraph


if __name__ == "__main__":
    compile(dynamic_subgraph, output=".build") 
