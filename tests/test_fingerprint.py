from pathlib import Path

from forge_lens import DataForgeLoader


def test_fingerprint_returns_string(loaded_loader):
    fp = loaded_loader.fingerprint()
    assert isinstance(fp, str)
    assert len(fp) == 12


def test_fingerprint_stable_on_reload(fixtures_root):
    """Same data loaded twice produces the same fingerprint."""
    a = DataForgeLoader(fixtures_root).load().fingerprint()
    b = DataForgeLoader(fixtures_root).load().fingerprint()
    assert a == b


def test_fingerprint_differs_for_different_dirs(fixtures_root):
    """Different data directories produce different fingerprints."""
    real = Path(__file__).parent / "fixtures_real"
    a = DataForgeLoader(fixtures_root).load().fingerprint()
    b = DataForgeLoader(real).load().fingerprint()
    assert a != b
