import pytest
from kivy.tests.fixtures import kivy_app

@pytest.fixture(scope='session')
def assets_dir():
    from pathlib import Path
    return Path(__file__).parents[1] / 'assets'

