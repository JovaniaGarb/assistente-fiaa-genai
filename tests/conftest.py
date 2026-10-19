import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from assistente_fiaa.pipeline import Assistente  # noqa: E402


@pytest.fixture
def assistente(tmp_path):
    return Assistente(log_dir=tmp_path)


@pytest.fixture
def fabrica(tmp_path):
    def _f(provider=None):
        return Assistente(provider=provider, log_dir=tmp_path)
    return _f
