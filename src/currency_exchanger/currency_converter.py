from dataclasses import dataclass

from .cer_providers import ExchangeRateProvider
from .data_structures import Sccs, Erm
from .utils import is_valid_cc


@dataclass
class CConfig:
    erm: Erm
    sccs: Sccs
    provider: ExchangeRateProvider


class CurrencyConverter:
    def __init__(self, config: CConfig):
        self.erm = config.erm
        self.sccs = config.sccs
        self.provider = config.provider

    def exchange(self, base_ccode: str, target_ccode: str, amount: float) -> float:
        """
        Converts amount of base currency code to amount of target code

        :param base_ccode: currency code need to be conveerted
        :param target_ccode: currency code to convert to
        :param amount: amount ot base code to convert
        """
        pair = (base_ccode, target_ccode)

        is_valid_cc(base_ccode)
        is_valid_cc(target_ccode)
        is_valid_amount(amount)
        not_supported = list(filter(lambda item: not item[1], zip(pair, self.sccs.mcontains(pair))))

        if not_supported:
            raise KeyError(f'Currencies {[item[0] for item in not_supported]} not supported')

        cer = self.erm.get(pair, None)

        if cer is None:
            # Could not find exchange rate in Erm, might be unfilled.
            # Then fetch from resource directly and update ERM if successful
            cer = self.provider.fetch_cer(*pair)

            if not cer:
                raise KeyError(f'Exchange rate of {pair} not found')

            self.erm[pair] = cer

        return cer * amount


def is_valid_amount(amount: float) -> bool:
    if amount < 0:
        raise ValueError(f'Expected amount to be > 0, given {amount}')
    return True
