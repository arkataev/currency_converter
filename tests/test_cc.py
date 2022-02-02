import pytest
from currency_converter import cc


@pytest.mark.parametrize('value, expected', [
    ('USD', True),
    ('USDC', False),
    ('1FD', False)
])
def test_is_valid_cc(value, expected):
    assert cc.is_valid_cc(value) == expected


@pytest.mark.parametrize('value, expected', [
    (1.0, 3.0, 3.0),
    (4.0, 0.5, 2.0),
    (2, -1, raise_error),
    (-1, 0, raise_error),
    (0, 0, 0.0)
])
def test_exchange(exchange_rate, amount, expected):
    assert cc.exchange(exchange_rate, amount) == expected
