from forge_lens import Query


def test_of_type_filters_by_tag(loaded_loader):
    results = Query(loaded_loader).of_type("EntityClassDefinition").all()
    assert len(results) > 0
    assert all(el.tag == "EntityClassDefinition" for el in results)


def test_where_filters_by_attribute(loaded_loader):
    results = Query(loaded_loader).of_type("EntityClassDefinition").where("__name", "ship_a").all()
    assert len(results) == 1
    assert results[0].get("__name") == "ship_a"


def test_all_returns_list(loaded_loader):
    result = Query(loaded_loader).all()
    assert isinstance(result, list)


def test_first_returns_element(loaded_loader):
    result = Query(loaded_loader).of_type("EntityClassDefinition").first()
    assert result is not None
    assert result.tag == "EntityClassDefinition"


def test_first_returns_none_when_no_match(loaded_loader):
    result = Query(loaded_loader).of_type("NonExistentType").first()
    assert result is None


def test_count_returns_int(loaded_loader):
    count = Query(loaded_loader).of_type("EntityClassDefinition").count()
    assert isinstance(count, int)
    assert count > 0


def test_chain_of_type_where_all(loaded_loader):
    results = Query(loaded_loader).of_type("EntityClassDefinition").where("__name", "ship_b").all()
    assert len(results) == 1
    assert results[0].get("__name") == "ship_b"
