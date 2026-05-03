from pathlib import Path

import pytest

from forge_lens import DataForgeLoader


@pytest.fixture
def fixtures_root() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def loaded_loader(fixtures_root: Path) -> DataForgeLoader:
    return DataForgeLoader(fixtures_root).load()
