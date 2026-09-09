# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

@dataclass(frozen=True)
class Checkpoint:
    position: str
    complete: bool

@dataclass(frozen=True)
class RecordEnvelope:
    local_id: str
    source_version: str
    observed_at: str
    payload: Mapping[str, Any]

@dataclass(frozen=True)
class ConnectorContext:
    workspace_id: str
    source_id: str
    allowed_destinations: tuple[str, ...]
    secrets: Mapping[str, str]

@runtime_checkable
class Connector(Protocol):
    manifest: Mapping[str, Any]
    def discover(self, context: ConnectorContext) -> Mapping[str, Any]: ...
    def read(self, context: ConnectorContext, checkpoint: Checkpoint | None) -> Iterable[tuple[RecordEnvelope, Checkpoint]]: ...

REQUIRED_CAPABILITIES = {"direction", "entities", "full_read", "incremental", "deletions", "schema_discovery", "auth", "write_operations", "rate_limits", "consistency", "checkpoint", "validation_status", "platform_compatibility"}

def validate_connector(connector: Connector, context: ConnectorContext) -> list[RecordEnvelope]:
    if not isinstance(connector, Connector): raise TypeError("connector does not satisfy the protocol")
    missing = REQUIRED_CAPABILITIES - set(connector.manifest)
    if missing: raise ValueError(f"manifest missing: {', '.join(sorted(missing))}")
    if connector.manifest["direction"] not in {"read", "write", "bidirectional"}: raise ValueError("invalid direction")
    discovered = connector.discover(context)
    if not isinstance(discovered, Mapping): raise TypeError("discover must return a mapping")
    records: list[RecordEnvelope] = []; positions: set[str] = set(); final = False
    for record, checkpoint in connector.read(context, None):
        if checkpoint.position in positions: raise ValueError("checkpoint did not advance")
        positions.add(checkpoint.position); final = checkpoint.complete
        if not record.local_id or not record.source_version: raise ValueError("stable local_id and source_version are required")
        records.append(record)
    if records and not final: raise ValueError("last checkpoint must mark a complete extraction")
    return records
