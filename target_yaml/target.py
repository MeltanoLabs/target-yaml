"""Yaml target class."""

from singer_sdk.target_base import Target
from singer_sdk import typing as th

from target_yaml.sinks import (
    YamlSink,
)


class TargetYaml(Target):
    """A Singer target that generates YAML files."""

    name = "target-yaml"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "file_naming_scheme",
            th.StringType,
            description=(
                "The scheme with which output files will be named. "
                "Naming scheme may leverage any of the following substitutions: \n\n"
                "- `{stream_name}`"
                "- `{datestamp}`"
                "- `{timestamp}`"
            ),
        ),
        th.Property(
            "datestamp_format",
            th.StringType,
            description=(
                "A format string to use when outputting the `{datestamp}` string. "
                "See [TODO: tbd] for reference."
            ),
        ),
        th.Property(
            "timestamp_format",
            th.StringType,
            description=(
                "A format string to use when outputting the `{timestamp}` string. "
                "See [TODO: tbd] for reference."
            ),
        ),
        th.Property(
            "stream_maps",
            th.StringType,
            description=(
                "Allows inline stream transformations and aliasing. "
                "For more information see: "
                "https://sdk.meltano.com/en/latest/stream_maps.html"
            ),
        ),
    ).to_dict()
    default_sink_class = YamlSink
