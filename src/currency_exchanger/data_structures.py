from typing import MutableMapping, Tuple, Optional, MutableSet, Iterator, List, Set, Iterable

from .storage import IStorage


class Erm(MutableMapping):
    """
    Exchange Rates Mapping

    Maps currency codes pair to related exchange rate. Default exchange rate is 0.0.
    Equal currencies exchange rate is always set to 1
    """
    def __init__(self, cc_pairs: Optional[Iterable[Tuple[str, str]]] = None):
        self._erm: [Tuple[str, str], float] = {}
        if cc_pairs:
            for pair in cc_pairs:
                self[pair] = 0.0

    def __getitem__(self, cc_pair: Tuple[str, str]) -> Optional[float]:
        return self._erm.get(cc_pair, None)

    def __setitem__(self, cc_pair: Tuple[str, str], cer: float):
        self._erm[cc_pair] = 1.0 if cc_pair[0] == cc_pair[1] else cer

    def __delitem__(self, cc_pair: Tuple[str, str]):
        del self._erm[cc_pair]

    def __iter__(self) -> Iterator[Tuple[str, str]]:
        return iter(self._erm)

    def __len__(self):
        return len(self._erm)

    def update(self, erm: 'Erm', **kwargs) -> None:
        self._erm.update(erm)


class Sccs(MutableSet):
    """Supported currency codes set"""

    def __init__(self, *args: [str]):
        self._sccs: Set[str] = set()
        if args:
            for arg in args:
                self._sccs.add(arg)

    def __iter__(self) -> Iterator:
        return iter(self._sccs)

    def __contains__(self, item) -> bool:
        return item in self._sccs

    def mcontains(self, items: Iterable[str]) -> List[bool]:
        return [item in self for item in items]

    def add(self, value: str) -> None:
        self._sccs.add(value)

    def discard(self, value: str) -> None:
        self._sccs.remove(value)

    def __len__(self):
        return len(self._sccs)


class PersistentErm(Erm):
    """Erm available to store and load exchange rates using persistent storage"""
    def __init__(self, storage: IStorage, *args, **kwargs):
        self.storage = storage
        super().__init__(*args, **kwargs)

    def __setitem__(self, cc_pair: Tuple[str, str], cer: float):
        self.storage.put(cc_pair, 1.0 if cc_pair[0] == cc_pair[1] else cer)
        super().__setitem__(cc_pair, cer)

    def __getitem__(self, cc_pair: Tuple[str, str]) -> Optional[float]:
        cer = self._erm.get(cc_pair, None)
        if not cer:
            cer = self.storage.get(cc_pair)
        return cer
