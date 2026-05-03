import json
import xml.etree.ElementTree as ET

from forge_lens.export import to_csv, to_dict, to_dicts, to_json


def _make_elem(tag: str, attribs: dict, children: list | None = None) -> ET.Element:
    el = ET.Element(tag, attribs)
    for child in children or []:
        el.append(child)
    return el


def test_to_dict_flat():
    el = _make_elem("EntityClassDefinition", {"__ref": "abc", "__name": "foo"})
    d = to_dict(el)
    assert d == {"__ref": "abc", "__name": "foo"}


def test_to_dict_with_children():
    child = _make_elem("Child", {"x": "1"})
    el = _make_elem("Parent", {"id": "p1"}, [child])
    d = to_dict(el)
    assert "_children" in d
    assert d["_children"][0]["x"] == "1"


def test_to_dicts_returns_list():
    els = [_make_elem("Foo", {"a": "1"}), _make_elem("Foo", {"a": "2"})]
    result = to_dicts(els)
    assert len(result) == 2
    assert result[0]["a"] == "1"


def test_to_json_valid():
    els = [_make_elem("Foo", {"a": "1", "b": "2"})]
    j = to_json(els)
    parsed = json.loads(j)
    assert parsed[0]["a"] == "1"


def test_to_csv_with_fields():
    els = [
        _make_elem("Rec", {"__ref": "u1", "__type": "T", "__path": "p1"}),
        _make_elem("Rec", {"__ref": "u2", "__type": "T", "__path": "p2"}),
    ]
    csv_out = to_csv(els, fields=["__ref", "__type"])
    lines = csv_out.strip().splitlines()
    assert lines[0] == "__ref,__type"
    assert "u1" in lines[1]


def test_to_csv_auto_fields():
    els = [_make_elem("Rec", {"a": "1", "b": "2"})]
    csv_out = to_csv(els)
    assert "a" in csv_out
    assert "b" in csv_out


def test_to_csv_empty_returns_empty_string():
    assert to_csv([]) == ""


def test_to_csv_drops_children_silently():
    child = _make_elem("Child", {"x": "1"})
    el = _make_elem("Parent", {"id": "p1"}, [child])
    csv_out = to_csv([el], fields=["id"])
    assert "_children" not in csv_out
