import os
from typing import Optional

import requests


class ExchangeRateProvider:
    def fetch_cer(self, base_ccode: str, target_ccode: str) -> Optional[float]:
        pass


class FreeCurrencyRateProvider(ExchangeRateProvider):
    api = 'https://freecurrencyapi.net/api/v2/latest'

    def fetch_cer(self, base_ccode: str, target_ccode: str) -> Optional[float]:
        """
        NB! This is very simplified fetching procedure as it's not considering any connection management,
        retrying policies and data validation.

        Fetching can also be optimized. freecurrencyapi returns all available exchange rates
        for a given base currency code, therefore such responses could be cached in memory for 30 sec (this is
        a refresh rate of the freecurrencyapi).
        """
        api_key = os.environ.get('FREECURRENCY_API', '2b836850-872a-11ec-9637-f9d7ca27317e')
        response = requests.get(self.api, params={'base_currency': base_ccode, 'apikey': api_key}, timeout=5)
        data = response.json().get('data', {})
        return data.get(target_ccode, None)
