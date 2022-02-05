from dataclasses import dataclass

from .data_structures import Sccs, Erm


@dataclass
class CConfig:
    erm: Erm
    sccs: Sccs


class CurrencyConverter:
    def __init__(self, config: CConfig):
        self.erm = config.erm
        self.sccs = config.sccs

    def exchange(self, code_x: str, code_y: str, amount: float) -> float:
        pair = (code_x, code_y)

        is_valid_amount(amount)
        list(map(is_valid_cc, pair))

        not_supported = list(filter(lambda item: not item[1], zip(pair, self.sccs.mcontains(pair))))

        if not_supported:
            raise KeyError(f'Currencies {[item[0] for item in not_supported]} not supported')

        cer = self.erm.get(pair, None)

        if cer is None:
            raise KeyError(f'Exchange rate of {pair} not found')

        return cer * amount


def is_valid_amount(amount: float) -> bool:
    if amount < 0:
        raise ValueError(f'Expected amount to be > 0, given {amount}')
    return True


def is_valid_cc(currency_code: str) -> bool:
    """Checks if currency code complies to ISO 4217"""
    if not len(currency_code) == 3:
        raise ValueError(f'Expected {currency_code} length is 3, got {len(currency_code)}')
    elif not currency_code.isupper():
        raise ValueError(f'Expected {currency_code} to be upper case')
    return True
