from unittest import mock

import pytest

from currency_exchanger.data_structures import Erm, Sccs
from currency_exchanger.cer_providers import ExchangeRateProvider

pytest_plugins = ("celery.contrib.pytest", )


@pytest.fixture
def erm() -> Erm:
    return mock.create_autospec(Erm, instance=True)


@pytest.fixture
def sccs():
    return mock.create_autospec(Sccs, instance=True)


@pytest.fixture
def provider():
    return mock.create_autospec(ExchangeRateProvider, instance=True)
