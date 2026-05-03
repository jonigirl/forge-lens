"""
loader.py — scan and load extracted DataForge XML directories.

Expected layout (produced by unforge / unp4k):
    <root>/
        Data/
            Libs/
                Foundry/
                    Records/
                        .../*.xml
            ...

Usage:
    loader = DataForgeLoader(r"C:/path/to/extracted")
    loader.load()
    # loader.records: dict[str, list[ET.Element]]  keyed by record type name
"""

from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path


class DataForgeLoader:
    """Loads DataForge XML records from an extracted game data directory."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.records: dict[str, list[ET.Element]] = {}
        self._files: list[Path] = []

    def load(self, glob: str = "**/*.xml") -> DataForgeLoader:
        """Walk root, parse every XML file, bucket elements by record type.

        Handles two XML layouts:

        * **Real DataForge** (unforge output): the root element IS the record,
          identified by a ``__type`` attribute (e.g. ``__type="CraftingBlueprintRecord"``).
        * **Wrapped/synthetic**: the root element is a container (e.g. ``<DCBRecords>``),
          and the records are its direct children.  Child type is read from the
          ``__type`` attribute when present, otherwise from the element tag.
        """
        self.records.clear()
        self._files.clear()
        for path in self.root.glob(glob):
            self._files.append(path)
            try:
                tree = ET.parse(path)
            except ET.ParseError:
                continue
            root = tree.getroot()
            type_attr = root.get("__type")
            if type_attr:
                # Real DataForge: root element is the record
                self.records.setdefault(type_attr, []).append(root)
            else:
                # Wrapped format: iterate children
                for elem in root:
                    type_key = elem.get("__type") or elem.tag
                    self.records.setdefault(type_key, []).append(elem)
        return self

    @property
    def record_types(self) -> list[str]:
        """Sorted list of record type names present in the loaded data."""
        return sorted(self.records.keys())

    def fingerprint(self) -> str:
        """Return a short hash representing the current loaded data state.

        Based on the sorted list of file paths and sizes.  Compare across
        sessions or after a game patch to detect when the DataForge data has
        changed and a reload is needed.

        Returns a 12-character hex string (48-bit SHA-256 prefix).
        """
        h = hashlib.sha256()
        for path in sorted(self._files):
            h.update(f"{path.name}:{path.stat().st_size}\n".encode())
        return h.hexdigest()[:12]

    def __len__(self) -> int:
        return sum(len(v) for v in self.records.values())

    def __repr__(self) -> str:
        return f"DataForgeLoader({self.root!r}, {len(self)} records, {len(self.records)} types)"
