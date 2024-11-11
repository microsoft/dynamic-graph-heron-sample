# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json

from azure.ai.ml import Input, Output
from azure.ai.ml.dsl._group_decorator import group

from mldesigner.dsl import dynamic

from components import train_model, validate, single_output_condition_func, merge_folders

# define multiple outputs for dynamic subgraph with @group decorator
@group
class DynamicSubgraphOutputs:
    output_model: Output(type="uri_folder")
    output_metric: Output(type="uri_folder")
    condition_output: Output(type="boolean", is_control=True)

ENVIRONMENT_DICT = dict(
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
    conda_file={
        "name": "default_environment",
        "channels": ["defaults"],
        "dependencies": [
            "python=3.9.16",
            "pip=21.2.2",
            {
                "pip": [
                    "--extra-index-url=https://pkgs.dev.azure.com/azure-sdk/public/_packaging/azure-sdk-for-python/pypi/simple/",
                    "azure-ai-ml==1.6.0a20230317001",
                    "azure-core==1.25.1",
                    "azure-common==1.1.28",
                    "azure-identity==1.11.0",
                    "azure-ml-component==0.9.18.post2",
                    "azureml-core==1.45.0.post2",
                    "azureml-mlflow==1.49.0",
                    "mldesigner==0.1.0b12",
                    "mlflow==2.1.1",
                    "mlflow-skinny==2.3.2",
                    "mltable==1.0.0",
                    "wheel==0.38.4"
                ]
            },
        ],
    }
)


@dynamic(environment=ENVIRONMENT_DICT)
def dynamic_subgraph(
    input_silos: Input(type="uri_file"), valid_data: Input(type="uri_file")
) -> DynamicSubgraphOutputs:
    """A dynamic subgraph that trains model and validates it multiple times according to specified input.

    :param input_silos: A file with a list of input silos.
    :param valid_data: Data to validate the model.
    """
    # Read list of silos from a json file input
    # Note: calling `pipeline_input.result()` inside @dynamic will return actual value of the input.
    # In this case, input_silos is an PipelineInput object, so we need to call `result()` to get the actual value.

    model_results = {}
    metric_results = {}
    with open(input_silos.result()) as fin:
        silos = json.load(fin)

    for silo in silos:
        train_node = train_model(silo=silo)
        validate_node = validate(
            model=train_node.outputs.output_model, silo=silo, valid_data=valid_data
        )

        model_results[silo] = train_node.outputs.output_model
        metric_results[silo] = validate_node.outputs.output_metric 

    condition_node = single_output_condition_func(address="h")
    merge_models = merge_folders(create_subfolder_for_each_input=True, **model_results)
    merge_metrics = merge_folders(create_subfolder_for_each_input=True, **metric_results)

    return {
        "output_model": merge_models.outputs.merged_folder,
        "output_metric": merge_metrics.outputs.merged_folder,
        "condition_output": condition_node.outputs.output,
    }
    # Note: returning DynamicSubgraphOutputs object like this is not supported currently.
    # return DynamicSubgraphOutputs(
    #     output_model: train_node.outputs.output_model,
    #     output_metric: validate_node.outputs.output_metric,
    #     condition_output: condition_node.outputs.output,
    # )