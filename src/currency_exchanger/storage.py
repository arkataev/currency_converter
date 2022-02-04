from operator import itemgetter
from typing import List


class IStorage:
    def put(self, key, value):...

    def get(self, key): ...

    def mget(self, keys: List) -> List: ...


class MemStorage(IStorage):
    def __init__(self):
        self._storage = {}

    def put(self, key, value):
        self._storage[key] = value

    def get(self, key):
        return self._storage.get(key)

    def mget(self, keys: List) -> List:
        get = itemgetter(*keys)
        return get(self._storage)


class RedisStorage(IStorage):
    pass
