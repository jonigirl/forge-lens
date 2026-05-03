from forge_lens.schema import describe, known_types


def test_known_types_returns_sorted_list():
    types = known_types()
    assert isinstance(types, list)
    assert types == sorted(types)
    assert "EntityClassDefinition" in types
    assert "CraftingBlueprintRecord" in types


def test_describe_known_type_returns_dict():
    d = describe("EntityClassDefinition")
    assert isinstance(d, dict)
    assert "__ref" in d


def test_describe_unknown_type_returns_empty():
    d = describe("NonExistentType")
    assert d == {}
