"""
graph.py — UUID resolution and relationship traversal.

This is the core of the blueprint/contract/crafting pipeline ported from
open-strings/scripts/generate_enhancements_ini.py.

Key concepts:
    - DataForge records reference each other by UUID (__ref or __id attributes)
    - display names live in EntityClassDefinition / ObjectContainer records
    - crafting trees: blueprint record → ingredient list → sub-blueprint UUIDs

Usage:
    graph = Graph(loader)
    name = graph.resolve_name("some-uuid-string")
    tree = graph.crafting_tree("blueprint-uuid")
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

from forge_lens.loader import DataForgeLoader

_MAX_DEPTH = 10


def _poly_type(elem: ET.Element) -> str:
    """Return the effective polymorphic type of a DataForge element.

    Handles both old unforge output (``__polymorphicType`` attribute) and
    new unforge output where the concrete type is the element tag itself.
    """
    return elem.get("__polymorphicType") or elem.tag


class Graph:
    """UUID resolution and relationship traversal over a loaded DataForge set."""

    def __init__(self, loader: DataForgeLoader) -> None:
        self._loader = loader
        self._by_uuid: dict[str, ET.Element] = {}
        self._name_map: dict[str, str] = {}
        self._built = False

    def build(self) -> Graph:
        """Index all records by their __ref / __id UUID for O(1) lookup."""
        self._by_uuid.clear()
        self._name_map.clear()
        for elements in self._loader.records.values():
            for el in elements:
                for attr in ("__ref", "__id", "ref"):
                    uid = el.get(attr)
                    if uid:
                        self._by_uuid[uid] = el
                        break
        self._built = True
        return self

    def resolve(self, uuid: str) -> ET.Element | None:
        """Return the element with this UUID, or None."""
        if not self._built:
            self.build()
        return self._by_uuid.get(uuid)

    def resolve_name(self, uuid: str) -> str | None:
        """Return the human-readable display name for a UUID, or None."""
        if not self._built:
            self.build()
        el = self._by_uuid.get(uuid)
        if el is None:
            return None
        # Common name attributes across DataForge record types
        for attr in ("__name", "name", "displayName", "localizedName"):
            v = el.get(attr)
            if v:
                return v
        return None

    def crafting_tree(
        self,
        uuid: str,
        depth: int = 0,
        _seen: set | None = None,
    ) -> dict:
        """Return a nested crafting tree dict for a CraftingBlueprintRecord UUID.

        Guards against cycles via *_seen* and against runaway depth via
        *_MAX_DEPTH*.  Returns a safe empty dict if the UUID is not found.
        """
        empty: dict = {
            "uuid": uuid,
            "name": None,
            "produces": None,
            "ingredients": [],
            "sub_blueprints": [],
        }
        if not self._built:
            self.build()
        if _seen is None:
            _seen = set()
        if uuid in _seen or depth > _MAX_DEPTH:
            return empty
        new_seen = _seen | {uuid}

        el = self._by_uuid.get(uuid)
        if el is None:
            return empty

        produces = None
        ingredients: list[dict] = []
        sub_blueprints: list[dict] = []

        for child in el:
            pt = _poly_type(child)
            if pt == "CraftingProcess_Creation":
                produces = child.get("entityClass")
            elif pt == "CraftingCost_Resource":
                resource_uuid = child.get("resource")
                if resource_uuid:
                    ingredients.append(
                        {
                            "uuid": resource_uuid,
                            "name": self.resolve_name(resource_uuid),
                        }
                    )
                    res_el = self._by_uuid.get(resource_uuid)
                    if (
                        res_el is not None
                        and res_el.tag == "CraftingBlueprintRecord"
                        and resource_uuid not in new_seen
                    ):
                        sub_blueprints.append(
                            self.crafting_tree(resource_uuid, depth + 1, new_seen)
                        )

        return {
            "uuid": uuid,
            "name": self.resolve_name(uuid),
            "produces": produces,
            "ingredients": ingredients,
            "sub_blueprints": sub_blueprints,
        }

    def reward_pool(self, uuid: str) -> list[str]:
        """Return sorted display names of craftable items in a BlueprintPoolRecord.

        Returns an empty list if the UUID is not found or no names resolve.
        """
        if not self._built:
            self.build()
        el = self._by_uuid.get(uuid)
        if el is None:
            return []
        names: list[str] = []
        for reward in el.iter("BlueprintReward"):
            bp_uuid = reward.get("blueprintRecord")
            if not bp_uuid:
                continue
            bp_el = self._by_uuid.get(bp_uuid)
            if bp_el is None:
                continue
            for child in bp_el:
                if _poly_type(child) == "CraftingProcess_Creation":
                    entity_uuid = child.get("entityClass")
                    if entity_uuid:
                        name = self.resolve_name(entity_uuid)
                        if name and name not in names:
                            names.append(name)
                    break
        return sorted(names)

    def __repr__(self) -> str:
        return f"Graph({len(self._by_uuid)} indexed UUIDs, built={self._built})"
