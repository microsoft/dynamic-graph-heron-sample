# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
from uuid import uuid4
from pathlib import Path

from mldesigner import command_component, Input, Output


@command_component
def gen_silos(
    params: str,
    output: Output(type="uri_file"),
    **kwargs,
):
    """Generate a json serialized uri_file according to given params.
    For example, if params is "1,2,3", then the output will be a json serialized uri_file with content ["1", "2", "3"].
    """
    with open(Path(output), "w") as fout:
        json.dump(params.split(","), fout)
    print(f"Extra args: {kwargs}")


@command_component(
    environment="./component_env.yaml",
)
def single_output_condition_func(
    address: str,
) -> Output(type="boolean", is_control=True):
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
    print((Path(model) / "model").read_text())
    print((Path(metric) / "metric").read_text())
    print(condition)