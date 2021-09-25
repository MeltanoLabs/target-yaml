"""Yaml target sink class, which handles writing streams."""

import datetime
from functools import cached_property
from pathlib import Path
from typing import List

from jsonpath_ng import jsonpath, parse
from ruamel.yaml import YAML

from singer_sdk.sinks import BatchSink


yaml = YAML()


class YamlSink(BatchSink):
    """Yaml target sink class."""

    max_size = None  # We want all records in one batch

    @cached_property
    def parent_jsonpath_expr(self) -> str:
        return self.tap_config["jsonpath_insertion_parent"]

    @cached_property
    def timestamp_time(self) -> datetime.datetime:
        return datetime.datetime.now(tz=self.config["timestamp_tz_offset"])

    @property
    def filepath_replacement_map(self) -> dict[str, str]:
        return {
            "stream_name": self.stream_name,
            "datestamp": self.timestamp_time.strftime(
                self.tap_config[self.datestamp_format]
            ),
            "timestamp": self.timestamp_time.strftime(
                self.tap_config[self.timestamp_format]
            ),
        }

    def _json_path_search(self, json: dict, expr: str, singular: bool = True):
        path = parse(expr)
        matches = path.find(json)
        if singular:
            return matches[0]

        return matches

    def _get_insertion_parent_node(self, doc_dict: dict) -> List[dict]:
        parent_node = self._json_path_search(
            json=doc_dict, expr=self.parent_jsonpath_expr
        )
        if not isinstance(parent_node, jsonpath.DatumInContext):
            raise Exception("Nothing found by the given json-path")

        return parent_node

    @property
    def destination_path(self) -> Path:
        result = self.config["file_naming_scheme"]
        for key, val in self.filepath_replacement_map.items():
            replacement_pattern = "{" f"{key}" "}"
            if replacement_pattern in result:
                result = result.replace(replacement_pattern, val)

        return result

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written."""
        output_file: Path = self.destination_path
        new_contents: dict = {}
        if output_file.exists():
            new_contents = yaml.load_all(output_file.read_text())

        parent_node: List[dict] = self._get_insertion_parent_node(new_contents)
        if self.tap_config["overwrite_behavior"] == "replace_records":
            parent_node.clear()

        parent_node.extend(context["records"])

        output_file.write_text(str(yaml.dump(new_contents)), encoding="utf-8")
