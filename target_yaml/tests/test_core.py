"""Tests standard target features using the built-in SDK tests library."""

from singer_sdk.testing import TargetTestRunner, get_test_class
from singer_sdk.testing.suites import target_tests

from target_yaml.target import TargetYaml

DEFAULT_YAML_TEMPLATE = "metrics: {}"

SAMPLE_CONFIG = {
    "file_naming_scheme": "{stream_name}.yml",
    "record_insert_jsonpath": "$.metrics",
    "default_yaml_template": DEFAULT_YAML_TEMPLATE,
    "record_key_property_name": "id",
    "max_parallelism": 1,
}

TestTargetYaml = get_test_class(
    test_runner_class=TargetTestRunner,
    test_runner_kwargs=dict(target_class=TargetYaml, config=SAMPLE_CONFIG),
    test_suites=[target_tests],
)
