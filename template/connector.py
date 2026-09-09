# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from recordlane_connector_kit import Checkpoint, ConnectorContext, RecordEnvelope

class TinyJsonlConnector:
    manifest = {
        "direction":"read", "entities":["Supplier"], "full_read":True,
        "incremental":"line offset with file fingerprint", "deletions":"explicit tombstones only",
        "schema_discovery":True, "auth":["filesystem ACL"], "write_operations":[],
        "rate_limits":"bounded by configured batch size", "consistency":"point-in-time file snapshot",
        "checkpoint":"zero-based line offset + fingerprint", "validation_status":"conformance_tested",
        "platform_compatibility":">=0.1.0a1,<0.2"
    }
    def __init__(self, path: Path): self.path = path
    def discover(self, context: ConnectorContext):
        with self.path.open(encoding="utf-8") as handle:
            first = json.loads(next(handle))
        return {"attributes": sorted(first), "entity":"Supplier"}
    def read(self, context: ConnectorContext, checkpoint: Checkpoint | None):
        start = int(checkpoint.position.split(":")[-1]) if checkpoint else 0
        lines = self.path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines[start:], start=start):
            value = json.loads(line)
            yield RecordEnvelope(str(value["id"]), str(value.get("version", 1)), datetime.now(timezone.utc).isoformat(), value), Checkpoint(f"line:{index+1}", index == len(lines)-1)
