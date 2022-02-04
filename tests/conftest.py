import pytest
from currency_exchanger.data_structures import Erm, Sccs

@pytest.fixture
def erm() -> Erm:
    return Erm()

@pytest.fixture
def sccs():
    return Sccs()

