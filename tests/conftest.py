import pytest
from currency_exchanger.data_structures import Erm, Sccs

pytest_plugins = ("celery.contrib.pytest", )

@pytest.fixture
def erm() -> Erm:
    return Erm()

@pytest.fixture
def sccs():
    return Sccs()
