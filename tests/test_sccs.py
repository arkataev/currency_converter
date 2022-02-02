from src.currency_converter.sccs import Sccs
import pytest


@pytest.fixture
def sccs():
    return Sccs()


def test_sccs_contains(sccs):
    sccs.add('a')
    assert 'a' in sccs


def test_sccs_mcontains_all(sccs):
    sccs.add('a')
    sccs.add('b')
    assert all(sccs.mcontains(['a', 'b']))


def test_sccs_mcontains_any(sccs):
    sccs.add('a')
    assert any(sccs.mcontains(['a', 'b']))


def test_sccs_mcontains_none(sccs):
    assert not all(sccs.mcontains(['a', 'b']))
