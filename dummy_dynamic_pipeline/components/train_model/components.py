# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from uuid import uuid4
from pathlib import Path

from mldesigner import command_component, Input, Output
from file_helper import copy_files


@command_component
def gen_silos(
    params: str,
    output: Output(type="uri_file"),
):
    """Generate a json serialized uri_file according to given params.
    For example, if params is "1,2,3", then the output will be a json serialized uri_file with content ["1", "2", "3"].
    """
    with open(Path(output), "w") as fout:
        json.dump(params.split(","), fout)


@command_component
def single_output_condition(
    address: str,
) -> Output(type="boolean"):
    # validate the address is https or not
    result = address.startswith("https://")
    return result


@command_component
def train_model(
    silo: str,
    output_model: Output(type="uri_folder"),
):
    """Train a model for silo i."""
    lines = [
        f"silo: {silo}",
        f"model output path: {output_model}",
    ]

    for line in lines:
        print(line)

    # Do the train and save the trained model as a file into the output folder.
    # Here only output a dummy data for demo.
    model = str(uuid4())
    (Path(output_model) / "model").write_text(model)


@command_component
def validate(
    model: Input(type="uri_folder"),
    silo: str,
    valid_data: Input(type="uri_file"),
    output_metric: Output(type="uri_folder"),
):
    """Validate the model for silo i."""
    lines = [
        f"model: {model}",
        f"silo: {silo}",
        f"test data: {valid_data}",
        f"score output path: {output_metric}",
    ]

    for line in lines:
        print(line)

    (Path(output_metric) / "metric").write_text(silo)


@command_component
def consume_model(
    model: Input(type="uri_folder"),
    metric: Input(type="uri_folder"),
    condition: Input(type="boolean"),
):
    """Print the content of metric file in given folder."""
    print(condition)

@command_component
def merge_folders(
    merged_folder: Output(type="uri_folder"),
    create_subfolder_for_each_input: Input(type="boolean", optional=True),
    **kwargs,
):
    """This component merges a dynamic count of inputs into one output."""
    for input_name, input_folder in kwargs.items():
        print("Copying input {input_name}")
        dest_folder = Path(merged_folder)
        if create_subfolder_for_each_input:
            dest_folder /= input_name
        copy_files(src_folder=input_folder, dest_folder=dest_folder, preserve_structure=True)