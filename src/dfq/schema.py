"""
schema.py — known DataForge record types and field mappings.

This is intentionally minimal at v0.1 — it grows as the library is used.
Treat these as advisory hints, not a complete spec. DataForge schema changes
with every SC patch; the loader works on raw XML regardless.
"""

from __future__ import annotations

# Record types known to exist in SC DataForge extractions.
# Values are dicts of field_name → description for documentation purposes.
KNOWN_TYPES: dict[str, dict[str, str]] = {
    "EntityClassDefinition": {
        "__name": "Internal entity class name",
        "__ref": "UUID",
        "displayName": "Localisation key or raw display name",
    },
    "SCItemWeaponComponentParams": {
        "size": "Weapon size (1–9)",
        "damage": "Base damage",
    },
    "SCItemShipComponentParams": {
        "grade": "Component grade (A–F)",
        "size": "Component size",
    },
    "CraftingRecipe": {
        "__ref": "UUID of this recipe",
        "output": "UUID of output item",
        "craftingTime": "Time in seconds",
    },
    "SContractTemplate": {
        "__ref": "UUID",
        "missionName": "Mission type identifier",
    },
}


def describe(record_type: str) -> dict[str, str]:
    """Return known field descriptions for a record type."""
    return KNOWN_TYPES.get(record_type, {})


def known_types() -> list[str]:
    return sorted(KNOWN_TYPES.keys())
