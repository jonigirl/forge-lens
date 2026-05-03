from forge_lens import DataForgeLoader


def test_load_returns_self(fixtures_root):
    loader = DataForgeLoader(fixtures_root)
    result = loader.load()
    assert result is loader


def test_records_populated(loaded_loader):
    assert len(loaded_loader.records) > 0


def test_record_types_sorted(loaded_loader):
    types = loaded_loader.record_types
    assert types == sorted(types)


def test_len_returns_total(loaded_loader):
    total = sum(len(v) for v in loaded_loader.records.values())
    assert len(loaded_loader) == total


def test_empty_directory(tmp_path):
    loader = DataForgeLoader(tmp_path).load()
    assert loader.records == {}


def test_nonexistent_directory():
    loader = DataForgeLoader("/does/not/exist/dataforge").load()
    assert loader.records == {}


def test_malformed_xml_skipped(tmp_path):
    bad = tmp_path / "bad.xml"
    bad.write_text("<this is not valid xml <<>>", encoding="utf-8")
    loader = DataForgeLoader(tmp_path).load()
    assert loader.records == {}
