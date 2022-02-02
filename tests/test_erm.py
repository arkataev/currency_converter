from currency_converter.erm import Erm
import pytest

@pytest.fixture
def erm() -> Erm:
    return Erm()


@pytest.mark.parametrize('items, length', [
    (['USD', 'ABC', 'CBA'], 6),
    (['USD', 'ABC', 'CBA', 'AAA'], 12),
    ([], 0),
    (['ABC'], 0),
])
def test_erm_create(items, length):
    """
    Given N items
    And N > 1
    When new Erm is created
    Then len(erm) == N! / (N - 2)!
    """
    erm = Erm(*items)
    assert len(erm) == length


@pytest.mark.parametrize('cc', [
    [('USD', 'ABC'), 0.0],
    [('ABC', 'ABC'), 1],
])
def test_erm_add_get(cc, erm):
    erm[cc[0]] = cc[1]
    assert erm[cc[0]] == cc[1]


def test_iter_erm(erm):
    erm[('USD', 'ABC')] = 1
    erm[('ABC', 'ABC')] = 1
    assert list(erm) == [('USD', 'ABC'), ('ABC', 'ABC')]

