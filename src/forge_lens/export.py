"""
export.py — serialise DataForge query results to dict, JSON, or CSV.

Usage:
    results = Query(loader).of_type("EntityClassDefinition").all()
    json_str = to_json(results)
    csv_str  = to_csv(results, fields=["__name", "__ref", "displayName"])
"""

from __future__ import annotations

import csv
import io
import json
import xml.etree.ElementTree as ET


def to_dict(element: ET.Element) -> dict[str, str | list]:
    """Convert a single XML element to a plain dict (attributes + children)."""
    d: dict[str, str | list] = dict(element.attrib)
    children = [to_dict(child) for child in element]
    if children:
        d["_children"] = children
    return d


def to_dicts(elements: list[ET.Element]) -> list[dict]:
    """Convert a list of XML elements to a list of plain dicts."""
    return [to_dict(el) for el in elements]


def to_json(elements: list[ET.Element], indent: int = 2) -> str:
    """Serialise a list of XML elements to a JSON string."""
    return json.dumps(to_dicts(elements), indent=indent, ensure_ascii=False)


def to_csv(elements: list[ET.Element], fields: list[str] | None = None) -> str:
    """
    Serialise elements to CSV. If fields is None, derive columns from all
    attribute keys seen across all elements (sorted).
    """
    dicts = to_dicts(elements)
    flat = [{k: v for k, v in d.items() if not isinstance(v, list)} for d in dicts]
    if not flat:
        return ""
    if fields is None:
        all_keys: set[str] = set()
        for row in flat:
            all_keys.update(row.keys())
        fields = sorted(all_keys)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(flat)
    return buf.getvalue()
