"""
query.py — filter and select DataForge records by type and attribute.

Usage:
    q = Query(loader)
    results = q.of_type("SCItemWeaponComponentParams").where("size", "3").all()
    first   = q.of_type("EntityClassDefinition").where("__ref", "GATS_Hornet").first()
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections.abc import Callable

from dfq.loader import DataForgeLoader


class Query:
    """Chainable query interface over a loaded DataForgeLoader."""

    def __init__(self, loader: DataForgeLoader) -> None:
        self._loader = loader
        self._type: str | None = None
        self._filters: list[Callable[[ET.Element], bool]] = []

    def of_type(self, record_type: str) -> Query:
        """Select records of the given DataForge type name."""
        q = self._clone()
        q._type = record_type
        return q

    def where(self, attr: str, value: str) -> Query:
        """Filter to records where element attribute equals value."""
        q = self._clone()
        q._filters.append(lambda el, a=attr, v=value: el.get(a) == v)
        return q

    def where_fn(self, fn: Callable[[ET.Element], bool]) -> Query:
        """Filter using an arbitrary predicate."""
        q = self._clone()
        q._filters.append(fn)
        return q

    def all(self) -> list[ET.Element]:
        candidates = (
            self._loader.records.get(self._type, [])
            if self._type
            else [el for els in self._loader.records.values() for el in els]
        )
        return [el for el in candidates if all(f(el) for f in self._filters)]

    def first(self) -> ET.Element | None:
        results = self.all()
        return results[0] if results else None

    def count(self) -> int:
        return len(self.all())

    def _clone(self) -> Query:
        q = Query(self._loader)
        q._type = self._type
        q._filters = list(self._filters)
        return q
