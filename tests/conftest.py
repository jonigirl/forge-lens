from pathlib import Path

import pytest

from forge_lens import DataForgeLoader


@pytest.fixture
def fixtures_root() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def loaded_loader(fixtures_root: Path) -> DataForgeLoader:
    return DataForgeLoader(fixtures_root).load()


@pytest.fixture
def real_format_root() -> Path:
    """Fixtures in the real unforge format: root element IS the record."""
    return Path(__file__).parent / "fixtures_real"


@pytest.fixture
def real_loader(real_format_root: Path) -> DataForgeLoader:
    return DataForgeLoader(real_format_root).load()
