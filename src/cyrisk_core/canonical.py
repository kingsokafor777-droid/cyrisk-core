"""Stable JSON serialization and SHA-256 integrity helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel


def canonical_json(value: BaseModel | dict[str, Any]) -> str:
    """Return a stable, compact JSON representation of a validated record."""
    payload = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def content_hash(value: BaseModel | dict[str, Any]) -> str:
    """Return the lowercase SHA-256 digest of canonical JSON."""
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()
