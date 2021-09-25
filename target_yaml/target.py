"""Yaml target class."""

from singer_sdk.target_base import Target
from singer_sdk import typing as th

from target_yaml.sinks import (
    YamlSink,
)


class TargetYaml(Target):
    """Sample target for Yaml."""

    name = "target-yaml"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "filepath",
            th.StringType,
            description="The path to the target output file"
        ),
        th.Property(
            "file_naming_scheme",
            th.StringType,
            description="The scheme with which output files will be named"
        ),
    ).to_dict()
    default_sink_class = YamlSink
