from abc import abstractmethod
from typing import MutableMapping, Tuple, Optional, MutableSet, Iterator, List, Sequence

import redis


class Sccs(MutableSet):
    """Supported currency codes set"""

    def __iter__(self) -> Iterator:
        raise NotImplementedError

    def __contains__(self, cur_code: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def mcontains(self, cur_codes: Sequence[str]) -> List[bool]:
        raise NotImplementedError

    def add(self, cur_code: str) -> None:
        raise NotImplementedError

    def discard(self, cur_code: str) -> None:
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


class Erm(MutableMapping):
    """
    Exchange Rates mapping.
    Maps currency codes pair to correspondent exchange rate
    """

    def __setitem__(self, cc_pair: Tuple[str, str], cer: float):
        raise NotImplementedError

    def __getitem__(self, cc_pair: Tuple[str, str]) -> float:
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __delitem__(self, cc_pair: Tuple[str, str]):
        raise NotImplementedError

    def __contains__(self, cc_pair: Tuple[str, str]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def mget(self, cc_pairs: Sequence[Tuple[str, str]]) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def mcontains(self, cc_pairs: Sequence[Tuple[str, str]]) -> List[bool]:
        raise NotImplementedError


class RedisErm(Erm):
    _name = 'erm'

    def __init__(self, storage: redis.Redis):
        self._storage = storage

    def __len__(self):
        return self._storage.hlen(self._name)

    def __iter__(self):
        return iter(self._storage.hkeys(self._name))

    def __contains__(self, cc_pair: Tuple[str, str]):
        return self._storage.hexists(self._name, self._make_key(cc_pair))

    def __setitem__(self, cc_pair: Tuple[str, str], cer: float):
        self._storage.hset(self._name, self._make_key(cc_pair), 1.0 if cc_pair[0] == cc_pair[1] else cer)

    def __getitem__(self, cc_pair: Tuple[str, str]) -> Optional[float]:
        return self._storage.hget(self._name, self._make_key(cc_pair))

    def __delitem__(self, cc_pair: Tuple[str, str]):
        self._storage.hdel(self._name, self._make_key(cc_pair))

    def mget(self, cc_pairs: Sequence[Tuple[str, str]]) -> List:
        return self._storage.hmget(self._name, map(self._make_key, cc_pairs))

    def mcontains(self, cc_pairs: Sequence[Tuple[str, str]]) -> List[bool]:
        pipe = self._storage.pipeline()
        for pair in cc_pairs:
            pipe.hexists(self._name, self._make_key(pair))
        return pipe.execute()

    def values(self):
        return self._storage.hvals(self._name)

    def items(self):
        items = self._storage.hgetall(self._name)
        if items:
            return items.items()

    @staticmethod
    def _make_key(cc_pair: Tuple[str, str]):
        return '/'.join(cc_pair)


class RedisSccs(Sccs):
    _name = 'sccs'

    def __init__(self, storage: redis.Redis):
        self._storage = storage

    def add(self, cur_code: str) -> None:
        self._storage.sadd(self._name, cur_code)

    def discard(self, cur_code: str) -> None:
        self._storage.srem(self._name, cur_code)

    def mcontains(self, cur_codes: Sequence[str]) -> List[bool]:
        return self._storage.smismember(self._name, cur_codes)

    def __contains__(self, cur_code: str) -> bool:
        return self._storage.sismember(self._name, cur_code)

    def __len__(self):
        return self._storage.scard(self._name)

    def __iter__(self):
        return iter(self._storage.smembers(self._name))
