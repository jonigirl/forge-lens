"""Tests for Graph methods using real unforge XML format fixtures.

Real DataForge XML has the record as the ROOT element (not wrapped in DCBRecords).
CraftingProcess_Creation and CraftingCost_Resource are deep-nested — graph.py
must use iter() rather than iterating direct children.
"""

from forge_lens import Graph

# UUIDs matching real_format fixtures
RF_BP_UUID = "00000000-0000-0000-0000-000000000100"
RF_ENTITY_UUID = "00000000-0000-0000-0000-000000000101"
RF_RESOURCE_UUID = "00000000-0000-0000-0000-000000000102"
RF_POOL_UUID = "00000000-0000-0000-0000-000000000110"


def test_real_format_loader_buckets_by_type(real_loader):
    """Loader correctly uses __type attr on root to bucket real-format records."""
    assert "CraftingBlueprintRecord" in real_loader.record_types
    assert "EntityClassDefinition" in real_loader.record_types
    assert "BlueprintPoolRecord" in real_loader.record_types


def test_real_format_resolve(real_loader):
    graph = Graph(real_loader)
    el = graph.resolve(RF_BP_UUID)
    assert el is not None
    assert el.get("__type") == "CraftingBlueprintRecord"


def test_real_format_resolve_name_tag_fallback(real_loader):
    """resolve_name falls back to the instance name in the root tag."""
    graph = Graph(real_loader)
    # Entity has no __name attr — name comes from tag: EntityClassDefinition.test_item
    name = graph.resolve_name(RF_ENTITY_UUID)
    assert name == "test_item"


def test_real_format_crafting_tree_deep_nested(real_loader):
    """crafting_tree uses iter() to find CraftingProcess_Creation and
    CraftingCost_Resource buried 5+ levels deep in real DataForge XML."""
    graph = Graph(real_loader)
    tree = graph.crafting_tree(RF_BP_UUID)

    assert tree["uuid"] == RF_BP_UUID
    # Name from tag fallback
    assert tree["name"] == "BP_CRAFT_test_ammo"
    # Produces resolved from deeply-nested CraftingProcess_Creation
    assert tree["produces"] == RF_ENTITY_UUID
    # Ingredient resolved from deeply-nested CraftingCost_Resource
    assert len(tree["ingredients"]) == 1
    assert tree["ingredients"][0]["uuid"] == RF_RESOURCE_UUID


def test_real_format_reward_pool_deep_nested(real_loader):
    """reward_pool uses iter() to find BlueprintReward and CraftingProcess_Creation
    in real-format pool and blueprint records."""
    graph = Graph(real_loader)
    names = graph.reward_pool(RF_POOL_UUID)
    # Pool → blueprint (RF_BP_UUID) → CraftingProcess_Creation → entity test_item
    assert names == ["test_item"]


def test_blueprints_producing(real_loader):
    """blueprints_producing returns blueprints that craft a given entity."""
    graph = Graph(real_loader)
    results = graph.blueprints_producing(RF_ENTITY_UUID)
    assert len(results) == 1
    assert results[0].get("__ref") == RF_BP_UUID


def test_blueprints_producing_unknown_returns_empty(real_loader):
    graph = Graph(real_loader)
    assert graph.blueprints_producing("00000000-0000-0000-0000-999999999999") == []


def test_pools_containing(real_loader):
    """pools_containing returns pools that reference a given blueprint."""
    graph = Graph(real_loader)
    results = graph.pools_containing(RF_BP_UUID)
    assert len(results) == 1
    assert results[0].get("__ref") == RF_POOL_UUID


def test_pools_containing_unknown_returns_empty(real_loader):
    graph = Graph(real_loader)
    assert graph.pools_containing("00000000-0000-0000-0000-999999999999") == []
