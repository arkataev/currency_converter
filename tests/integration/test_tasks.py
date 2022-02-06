from unittest import mock
from currency_exchanger.tasks import refresh_currency


def test_refresh_currency_task_success():
    with mock.patch('currency_exchanger.tasks.FreeCurrencyRateProvider.fetch_cer') as resource:
        with mock.patch('currency_exchanger.tasks.RefreshCurrencyTask.on_success') as on_success:
            resource.return_value = 1
            refresh_currency.apply(args=('USD', 'RUB'))
            on_success.assert_called_once()


def test_refresh_currency_task_fail():
    with mock.patch('currency_exchanger.tasks.FreeCurrencyRateProvider.fetch_cer') as resource:
        with mock.patch('currency_exchanger.tasks.RefreshCurrencyTask.on_failure') as on_failure:
            resource.side_effect = Exception
            refresh_currency.apply(args=('USD', 'RUB'))
            on_failure.assert_called_once()
