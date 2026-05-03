"""
schema.py — known DataForge record types and field mappings.

This is intentionally minimal at v0.1 — it grows as the library is used.
Treat these as advisory hints, not a complete spec. DataForge schema changes
with every SC patch; the loader works on raw XML regardless.
"""

from __future__ import annotations

# Record types known to exist in SC DataForge extractions.
# Values are dicts of field_name → description for documentation purposes.
# Types confirmed from unforge output — 27 top-level types in a typical cache.
KNOWN_TYPES: dict[str, dict[str, str]] = {
    "EntityClassDefinition": {
        "__ref": "UUID of this entity",
        "__type": "Always 'EntityClassDefinition'",
        "__path": "Relative file path within the DataForge export",
        # Display name lives in tag: RecordType.InstanceName — split on '.' for instance name.
        # Localized display names (e.g. @LOC_xxx keys) are nested inside
        # Components > SAttachableComponentParams > AttachDef > Localization[@Name]
    },
    "CraftingBlueprintRecord": {
        "__ref": "UUID of this blueprint",
        "__type": "Always 'CraftingBlueprintRecord'",
        "__path": "Relative file path",
        # Output item:
        #   blueprint/CraftingBlueprint/processSpecificData
        #   /CraftingProcess_Creation[@entityClass]
        # Ingredients (use iter() — nested under tiers/recipe/costs):
        #   CraftingCost_Resource[@resource, @minQuality]
        #   CraftingCost_Select wraps options with CraftingCost_Resource
    },
    "BlueprintPoolRecord": {
        "__ref": "UUID of this reward pool",
        "__type": "Always 'BlueprintPoolRecord'",
        # Blueprint entries: blueprintRewards/BlueprintReward[@blueprintRecord, @weight]
    },
    "ContractTemplate": {
        "__ref": "UUID",
        "__type": "Always 'ContractTemplate'",
        "__path": "Relative file path",
        # Contract class, display info, properties, objective tokens nested inside
    },
    "ContractGenerator": {
        "__ref": "UUID",
        "__type": "Always 'ContractGenerator'",
    },
    "AmmoParams": {
        "__ref": "UUID",
        "__type": "Always 'AmmoParams'",
    },
    "MissionBrokerEntry": {
        "__ref": "UUID",
        "__type": "Always 'MissionBrokerEntry'",
    },
}


def describe(record_type: str) -> dict[str, str]:
    """Return known field descriptions for a record type."""
    return KNOWN_TYPES.get(record_type, {})


def known_types() -> list[str]:
    """Return a sorted list of record type names with known field descriptions."""
    return sorted(KNOWN_TYPES.keys())
