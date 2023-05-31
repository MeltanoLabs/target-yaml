# `target-yaml`

A Singer target that generates YAML files.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

## Capabilities

* `about`
* `stream-maps`
* `schema-flattening`

## Settings

| Setting                  | Required | Default | Description |
|:-------------------------|:--------:|:-------:|:------------|
| file_naming_scheme       | False    | None    | The scheme with which output files will be named. Naming scheme may leverage any of the following substitutions: <BR/><BR/>- `{stream_name}`- `{datestamp}`- `{timestamp}` |
| datestamp_format         | False    | %Y-%m-%d | A python format string to use when outputting the `{datestamp}` string. For reference, see: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes |
| timestamp_format         | False    | %Y-%m-%d.T%H%M%S | A python format string to use when outputting the `{timestamp}` string. For reference, see: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes |
| timestamp_timezone       | False    | UTC     | The timezone code or name to use when generating `{timestamp}` and `{datestamp}`. Defaults to 'UTC'. For a list of possible values, please see: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones |
| stream_maps              | False    | None    | Allows inline stream transformations and aliasing. For more information see: https://sdk.meltano.com/en/latest/stream_maps.html |
| record_insert_jsonpath   | False    | $.metrics | A jsonpath string determining the insertion point for new records. Currently, this must be the path to a map key which will be populated by a list of records. <BR/><BR/>For example '$.metrics' will populate the file with `metrics: [{<record1>},{<record2>},...]` <BR/><BR/>For JSONPath syntax help, see: https://jsonpath.com |
| record_key_property_name | False    | None    | A property in the record which will be used as the dictionary key.<BR/><BR/>If this property is provided, records will be written as key-value objects; if omitted, records are written as a list. |
| record_sort_property_name| False    | None    | A property in the record which will be used as a sort key.<BR/><BR/>If this property is omitted, records will not be sorted. |
| overwrite_behavior       | False    | replace_records | Determines the overwrite behavior if destination file already exists. Must be one of the following string values: <BR/><BR/>- `append_records` (default) - append records at the insertion point<BR/>- `replace_records` - replace all records at the insertion point<BR/>- `replace_file` - replace entire file using `default_yaml_template`<BR/> |
| default_yaml_template    | False    | None    | Text string to use for a yaml template file. This text will be used to create a new file if the destination file does not exist. |
| stream_map_config        | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled       | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth     | False    | None    | The max depth to flatten schemas. |

A full list of supported settings and capabilities is available by running: `target-yaml --about`

### Source Authentication and Authorization

## Usage

You can easily run `target-yaml` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Target Directly

```bash
target-yaml --version
target-yaml --help
# Test using the "Carbon Intensity" sample:
tap-carbon-intensity | target-yaml --config /path/to/target-yaml-config.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `target_yaml/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `target-yaml` CLI interface directly using `poetry run`:

```bash
poetry run target-yaml --help
```

### Testing with [Meltano](https://meltano.com/)

_**Note:** This target will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd target-yaml
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke target-yaml --version
# OR run a test `elt` pipeline with the Carbon Intensity sample tap:
meltano elt tap-carbon-intensity target-yaml
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the Meltano SDK to
develop your own Singer taps and targets.
