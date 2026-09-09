# SPDX-License-Identifier: Apache-2.0
import importlib.util
from pathlib import Path
from recordlane_connector_kit import ConnectorContext, validate_connector

ROOT=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location("tiny",ROOT/"template"/"connector.py")
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

def test_connector_template_passes_without_core_changes():
    connector=module.TinyJsonlConnector(ROOT/"template"/"sample.jsonl")
    records=validate_connector(connector,ConnectorContext("workspace","source",(),{}))
    assert [r.local_id for r in records] == ["tiny-1","tiny-2"]
    assert connector.manifest["write_operations"] == []
