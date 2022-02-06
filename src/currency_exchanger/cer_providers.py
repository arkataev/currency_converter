import os
from json import JSONDecodeError
from typing import Optional
import logging
import requests

logger = logging.getLogger(__name__)


class CerResourceError(Exception):
    pass


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
        a refresh rate of freecurrencyapi).
        """
        api_key = os.environ.get('FREECURRENCY_API')
        response = requests.get(self.api, params={'base_currency': base_ccode, 'apikey': api_key}, timeout=5)
        try:
             decoded = response.json()
        except JSONDecodeError:
            raise CerResourceError(f'Unexpected response {response.content}')

        if not response.ok:
            raise CerResourceError(f'Failed to get CER for {base_ccode, target_ccode} from resource {self.api}. '
                                   f'Reason: {decoded}. Status: {response.status_code}')

        data = decoded.get('data', None)

        if not data:
            logger.warning(f'No data found for {base_ccode, target_ccode} in {self.api} response. {decoded}')
            raise CerResourceError(f'Failed to get CER for {base_ccode, target_ccode} from resource {self.api}. '
                                   f'Reason: No data')

        return data.get(target_ccode, None)
