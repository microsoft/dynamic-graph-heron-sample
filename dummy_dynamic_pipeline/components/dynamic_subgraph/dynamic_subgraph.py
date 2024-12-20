# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json

from azure.ai.ml import Input, Output
from azure.ai.ml.dsl._group_decorator import group

from mldesigner.dsl import dynamic
from azure.ai.ml import MLClient
from azure.ai.ml.identity import AzureMLOnBehalfOfCredential

# define multiple outputs for dynamic subgraph with @group decorator
@group
class DynamicSubgraphOutputs:
    output_model: Output(type="uri_folder")
    output_metric: Output(type="uri_folder")
    condition_output: Output(type="boolean")


@dynamic()
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

    credential = AzureMLOnBehalfOfCredential()
    ml_client =  MLClient.from_config(credential=credential)
    train_model_func = ml_client.components.get(name="train_model")
    validate_func = ml_client.components.get(name="validate")
    single_output_condition_func = ml_client.components.get(name="single_output_condition")
    merge_folders_with_fix_inputs_func = ml_client.components.get(name="merge_folders_with_fix_inputs")
    
    model_results = {}
    metric_results = {}
    with open(input_silos.result()) as fin:
        silos = json.load(fin)

    for silo in silos:
        train_node = train_model_func(silo=silo)
        validate_node = validate_func(
            model=train_node.outputs.output_model, silo=silo, valid_data=valid_data
        )

        model_results[silo] = train_node.outputs.output_model
        metric_results[silo] = validate_node.outputs.output_metric 

    condition_node = single_output_condition_func(address="h")
    merge_models = merge_folders_with_fix_inputs_func(create_subfolder_for_each_input=True, **model_results)
    merge_metrics = merge_folders_with_fix_inputs_func(create_subfolder_for_each_input=True, **metric_results)

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