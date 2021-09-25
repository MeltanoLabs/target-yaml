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
                "A python format string to use when outputting the `{datestamp}` "
                "string. For reference, see: "
                "https://docs.python.org/3/library/datetime.html"
                "#strftime-and-strptime-format-codes"
            ),
            default="%Y-%m-%d",
        ),
        th.Property(
            "timestamp_format",
            th.StringType,
            description=(
                "A python format string to use when outputting the `{timestamp}` "
                "string. For reference, see: "
                "https://docs.python.org/3/library/datetime.html"
                "#strftime-and-strptime-format-codes"
            ),
            default="%Y-%m-%d.T%H%M%S",
        ),
        th.Property(
            "timestamp_timezone",
            th.StringType,
            description=(
                "The timezone code or name to use when generating "
                "`{timestamp}` and `{datestamp}`. "
                "Defaults to 'UTC'. For a list of possible values, please see: "
                "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
            ),
            default="UTC",
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
        # TODO: Currently will create all entries at the file root
        th.Property(
            "record_insert_jsonpath",
            th.StringType,
            description=(
                "A jsonpath string determining the insertion point for new records. "
                "For JSONPath syntax help, see: https://jsonpath.com"
            ),
            default="$",
        ),
        th.Property(
            "overwrite_behavior",
            th.StringType,
            description=(
                "Determines the overwrite behavior if destination file already exists. "
                "Must be one of the following string values: \n\n"
                "- `append_records` (default) - append records at the insertion point\n"
                "- `replace_records` - replace all records at the insertion point\n"
                "- `replace_file` - replace entire file using `default_yaml_template`\n"
            ),
            default="append_records",
        ),
        th.Property(
            "default_yaml_template",
            th.StringType,
            description=(
                "Text string to use for a yaml template file. "
                "This text will be used to create a new file if the destination "
                "file does not exist."
            ),
        ),
    ).to_dict()
    default_sink_class = YamlSink
