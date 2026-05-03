from forge_lens import Graph


def test_build_returns_self(loaded_loader):
    graph = Graph(loaded_loader)
    result = graph.build()
    assert result is graph


def test_resolve_returns_element(loaded_loader):
    graph = Graph(loaded_loader).build()
    el = graph.resolve("00000000-0000-0000-0000-000000000001")
    assert el is not None
    assert el.get("__ref") == "00000000-0000-0000-0000-000000000001"


def test_resolve_unknown_returns_none(loaded_loader):
    graph = Graph(loaded_loader).build()
    assert graph.resolve("00000000-0000-0000-0000-999999999999") is None


def test_resolve_name_returns_string(loaded_loader):
    graph = Graph(loaded_loader).build()
    name = graph.resolve_name("00000000-0000-0000-0000-000000000001")
    assert isinstance(name, str)
    assert len(name) > 0


def test_resolve_name_unknown_returns_none(loaded_loader):
    graph = Graph(loaded_loader).build()
    assert graph.resolve_name("00000000-0000-0000-0000-999999999999") is None


def test_repr_includes_uuid_count(loaded_loader):
    graph = Graph(loaded_loader).build()
    r = repr(graph)
    assert "indexed UUIDs" in r


# ── crafting_tree ─────────────────────────────────────────────────────────────

BP_UUID = "00000000-0000-0000-0000-000000000010"
ENTITY_UUID = "00000000-0000-0000-0000-000000000011"
RESOURCE_UUID = "00000000-0000-0000-0000-000000000012"
POOL_UUID = "00000000-0000-0000-0000-000000000020"
CYCLIC_UUID = "00000000-0000-0000-0000-000000000030"


def test_crafting_tree_returns_expected_structure(loaded_loader):
    graph = Graph(loaded_loader).build()
    tree = graph.crafting_tree(BP_UUID)

    assert tree["uuid"] == BP_UUID
    assert tree["produces"] == ENTITY_UUID
    assert len(tree["ingredients"]) == 1
    assert tree["ingredients"][0]["uuid"] == RESOURCE_UUID
    assert tree["ingredients"][0]["name"] == "Raw Iron"
    assert tree["sub_blueprints"] == []


def test_crafting_tree_unknown_uuid_returns_empty(loaded_loader):
    graph = Graph(loaded_loader).build()
    tree = graph.crafting_tree("00000000-0000-0000-0000-999999999999")

    assert tree["uuid"] == "00000000-0000-0000-0000-999999999999"
    assert tree["name"] is None
    assert tree["produces"] is None
    assert tree["ingredients"] == []
    assert tree["sub_blueprints"] == []


def test_crafting_tree_cycle_guard(loaded_loader):
    graph = Graph(loaded_loader).build()
    # bp_cyclic has resource pointing to itself — must not recurse infinitely
    tree = graph.crafting_tree(CYCLIC_UUID)

    assert tree["uuid"] == CYCLIC_UUID
    assert tree["sub_blueprints"] == []


# ── reward_pool ───────────────────────────────────────────────────────────────


def test_reward_pool_returns_expected_names(loaded_loader):
    graph = Graph(loaded_loader).build()
    names = graph.reward_pool(POOL_UUID)

    assert names == ["Iron Plate"]


def test_reward_pool_unknown_uuid_returns_empty(loaded_loader):
    graph = Graph(loaded_loader).build()
    assert graph.reward_pool("00000000-0000-0000-0000-999999999999") == []
