"""Yaml target sink class, which handles writing streams."""

import datetime
import pytz
import sys, os

from functools import cached_property
from pathlib import Path
from typing import Any, Dict, List, Union

from jsonpath_ng import jsonpath, parse
from ruamel.yaml import YAML

from singer_sdk.sinks import BatchSink


yaml = YAML()


class YamlSink(BatchSink):
    """Yaml target sink class."""

    max_size = sys.maxsize  # We want all records in one batch

    @cached_property
    def parent_jsonpath_expr(self) -> str:
        return self.config["record_insert_jsonpath"]

    @cached_property
    def timestamp_time(self) -> datetime.datetime:
        return datetime.datetime.now(
            tz=pytz.timezone(self.config["timestamp_timezone"])
        )

    @property
    def filepath_replacement_map(self) -> Dict[str, str]:
        return {
            "stream_name": self.stream_name,
            "datestamp": self.timestamp_time.strftime(self.config["datestamp_format"]),
            "timestamp": self.timestamp_time.strftime(self.config["timestamp_format"]),
        }

    def _json_path_search(self, json: dict, expr: str, singular: bool = True):
        path = parse(expr)
        matches = path.find(json)

        if len(matches) == 0:
            raise ValueError(
                f"Could not find jsonpath '{expr}' in JSON document body. "
                "Please verify the file path, `record_insert_jsonpath`, "
                f"and `default_yaml_template`. Body was: {repr(json)[0:1000]}"
            )

        if singular:
            return matches[0]

        return matches

    def _get_insertion_point_node(
        self, doc_dict: dict
    ) -> Union[List[dict], Dict[str, dict]]:
        parent_node = self._json_path_search(
            json=doc_dict, expr=self.parent_jsonpath_expr
        )
        if not isinstance(parent_node, jsonpath.DatumInContext):
            raise Exception("Nothing found by the given json-path")

        # With large files this can cause the system to crash:
        # self.logger.info(
        #     f"Found parent_node '{parent_node}' with "
        #     f"context '{parent_node.context}' with "
        #     f"context value '{parent_node.context.value}'"
        # )
        return parent_node.value

    @property
    def destination_path(self) -> Path:
        result = self.config["file_naming_scheme"]
        for key, val in self.filepath_replacement_map.items():
            replacement_pattern = "{" f"{key}" "}"
            if replacement_pattern in result:
                result = result.replace(replacement_pattern, val)

        return Path(result)

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written."""
        output_file: Path = self.destination_path
        self.logger.info(f"Writing to destination file '{output_file.resolve()}'...")
        new_contents: dict
        create_new = (
            self.config["overwrite_behavior"] == "replace_file"
            or not output_file.exists()
        )
        if not create_new:
            new_contents = yaml.load(output_file.read_text())
        elif "default_yaml_template" not in self.config:
            raise ValueError(
                "Config value `default_yaml_template` is required because either the "
                "file does not exist or `overwrite_behavior` = 'replace_file'."
            )

        else:
            new_contents = yaml.load(self.config["default_yaml_template"])

        parent_node: List[dict] = self._get_insertion_point_node(doc_dict=new_contents)

        if not isinstance(context["records"], list):
            raise ValueError(f"No values in records collection.")

        records: List[Dict[str, Any]] = context["records"]
        if "record_sort_property_name" in self.config:
            sort_property_name = self.config["record_sort_property_name"]
            records = sorted(records, key=lambda x: x[sort_property_name])

        if "record_key_property_name" in self.config:
            self.logger.info(
                "`record_key_property_name` setting exists. Writing as dict."
            )
            assert isinstance(
                parent_node, dict
            ), f"Expected 'dict', found {parent_node}"
            if self.config["overwrite_behavior"] == "replace_records":
                parent_node.clear()

            key_property_name = self.config["record_key_property_name"]
            for record in records:
                record_key = record.pop(key_property_name)
                parent_node[record_key] = record

        else:
            self.logger.info(
                "`record_key_property_name` setting does not exist. Writing as list."
            )
            assert isinstance(parent_node, list)
            if self.config["overwrite_behavior"] == "replace_records":
                parent_node.clear()

            self.logger.info(f"Writing {len(context['records'])} records to file...")
            parent_node.extend(context["records"])

        with open(output_file, "w", encoding="utf-8") as fp:
            yaml.dump(new_contents, stream=fp)
