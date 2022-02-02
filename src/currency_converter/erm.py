from itertools import permutations
from typing import MutableMapping, Tuple, Optional, Iterator

from .utils import is_valid_cc


class Erm(MutableMapping):
    """
    Exchange Rates Mapping

    Maps currency codes pair to related exchange rate. Default exchange rate is 0.0.
    Equal currencies exchange rate is always set to 1
    """
    def __init__(self, *codes: [str]):
        self._erm: [Tuple[str, str], float] = {}
        if codes and len(codes) > 1:
            pair: Tuple[str, str]
            for pair in permutations(codes, 2):
                self[pair] = 0.0

    def __getitem__(self, currency_codes: Tuple[str, str]) -> Optional[float]:
        return self._erm.get(currency_codes, None)

    def __setitem__(self, currency_codes: Tuple[str, str], cer: float):
        self._erm[currency_codes] = 1.0 if currency_codes[0] == currency_codes[1] else cer

    def __delitem__(self, currency_codes: Tuple[str, str]):
        del self._erm[currency_codes]

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(self._erm)

    def __len__(self):
        return len(self._erm)
