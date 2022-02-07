import pytest

from currency_exchanger.currency_converter import CurrencyConverter, CConfig, is_valid_cc, is_valid_amount


@pytest.fixture
def cc(erm, sccs, provider):
    conf = CConfig(erm, sccs, provider)
    return CurrencyConverter(conf)


@pytest.mark.parametrize('value', ['USDC', 1, 'abc'])
def test_is_not_valid_cc(value):
    with pytest.raises((ValueError, TypeError)):
        assert is_valid_cc(value)


def test_is_valid_cc():
    assert is_valid_cc("ABC")


def test_is_not_valid_amount():
    with pytest.raises((ValueError, TypeError)):
        assert is_valid_amount(-1.0)


def test_is_valid_amount():
    assert is_valid_amount(1.0)


@pytest.mark.parametrize('code_x, code_y, amount, cer, expected', [
    ('USD', 'EUR', 5.0, 2, 10.0),
    ('USD', 'EUR', 5.0, 0, 0),
    ('USD', 'EUR', 0.0, 1, 0),
])
def test_exchange(code_x, code_y, amount, cer, expected, cc):
    """
    Given code_x is valid and supported
    And code_y is valid and supported
    And amount is valid
    And code_x/code_y cer is not None
    When amount of code_x exchanged to code_y
    Then amount of code_y == amount of code_x * cer
    """
    cc.sccs.mcontains.return_value = [True, True]
    cc.erm.get.return_value = cer
    assert cc.exchange(code_x, code_y, amount) == expected


def test_exchange_not_supported(cc):
    """
    Given code_x and code_y are valid
    Given code_x or code_y is not supported
    When exchange happens
    Then ValueError is raised
    """
    cc.sccs.mcontains.return_value = [True, False]
    with pytest.raises(KeyError):
        cc.exchange('USD', 'EUR', 1.0)


def test_exchange_no_cer(cc):
    """
    Given code_x and code_y are valid
    Given code_x and code_y are supported
    Given no exchange rate for code_x and code_y
    When exchange happens
    Then KeyError is raised
    """
    cc.sccs.return_value = [True, True]
    cc.erm.get.return_value = None
    cc.provider.fetch_cer.return_value = None
    with pytest.raises(KeyError):
        cc.exchange('USD', 'EUR', 1.0)
    assert cc.provider.fetch_cer.called


def test_exchange_cer_found_in_provider(cc):
    cc.sccs.return_value = [True, True]
    cc.erm.get.return_value = None
    cc.provider.fetch_cer.return_value = 1.0
    cc.exchange('USD', 'EUR', 1.0)
    assert cc.provider.fetch_cer.called
    assert cc.erm.__setitem__.called