from typing import MutableSet, Iterator, List, Set, Iterable


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


def is_supported_cc(currency_code: str) -> bool:
    """Checks if currency code is present in SCCS"""

