"""Small local CLI for validating and hashing RiskScenario JSON."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

from cyrisk_core.canonical import canonical_json, content_hash
from cyrisk_core.models import RiskScenario


def _load_scenario(path: Path) -> RiskScenario:
    """Load and validate a scenario JSON document."""
    with path.open(encoding="utf-8") as handle:
        return RiskScenario.model_validate(json.load(handle))


def _hash_command(path: Path) -> int:
    scenario = _load_scenario(path)
    print(content_hash(scenario))
    return 0


def _canonical_command(path: Path) -> int:
    scenario = _load_scenario(path)
    print(canonical_json(scenario))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the local-only CLI and return an explicit exit code."""
    parser = argparse.ArgumentParser(prog="cyrisk-core")
    parser.add_argument("command", choices=("hash", "canonical"))
    parser.add_argument("scenario", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "hash":
            return _hash_command(args.scenario)
        return _canonical_command(args.scenario)
    except (OSError, ValidationError, json.JSONDecodeError) as error:
        parser.error(str(error))
