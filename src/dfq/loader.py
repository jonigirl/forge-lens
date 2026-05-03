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

import xml.etree.ElementTree as ET
from pathlib import Path


class DataForgeLoader:
    """Loads DataForge XML records from an extracted game data directory."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.records: dict[str, list[ET.Element]] = {}
        self._files: list[Path] = []

    def load(self, glob: str = "**/*.xml") -> DataForgeLoader:
        """Walk root, parse every XML file, bucket elements by tag."""
        self.records.clear()
        self._files.clear()
        for path in self.root.glob(glob):
            self._files.append(path)
            try:
                tree = ET.parse(path)
            except ET.ParseError:
                continue
            for elem in tree.getroot():
                tag = elem.tag
                self.records.setdefault(tag, []).append(elem)
        return self

    @property
    def record_types(self) -> list[str]:
        return sorted(self.records.keys())

    def __len__(self) -> int:
        return sum(len(v) for v in self.records.values())

    def __repr__(self) -> str:
        return f"DataForgeLoader({self.root!r}, {len(self)} records, {len(self.records)} types)"
