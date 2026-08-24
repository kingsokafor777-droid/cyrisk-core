"""Fail closed if the built wheel lacks public Cyrisk source modules."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
REQUIRED = {
    "cyrisk_core/__init__.py",
    "cyrisk_core/canonical.py",
    "cyrisk_core/models.py",
    "cyrisk_core/py.typed",
}


def main() -> int:
    """Check the newest wheel contains required public source files."""
    wheels = sorted(DIST.glob("cyrisk_core-*.whl"))
    if len(wheels) != 1:
        print(f"expected one wheel, found {len(wheels)}", file=sys.stderr)
        return 1
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
    missing = REQUIRED - names
    if missing:
        print(f"wheel missing files: {sorted(missing)}", file=sys.stderr)
        return 1
    print(f"VALID wheel={wheels[0].name} files={len(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
