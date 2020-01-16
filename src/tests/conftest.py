import pytest


@pytest.fixture(scope='session')
def assets_dir():
    from pathlib import Path
    return Path(__file__).parents[1] / 'assets'
