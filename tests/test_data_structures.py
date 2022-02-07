import os
from unittest import mock

import pytest
from redis import Redis

from currency_exchanger.data_structures import RedisSccs, RedisErm


@pytest.fixture(scope='module', autouse=True)
def env():
    os.environ.update({'REDIS_SCCS_NAME': 'test_sccs', 'REDIS_ERM_NAME': 'test_erm'})


@pytest.fixture
def redis_mock():
    return mock.create_autospec(Redis, instance=True)


@pytest.fixture
def redis_erm(redis_mock):
    return RedisErm(redis_mock)


@pytest.fixture
def redis_sccs(redis_mock):
    return RedisSccs(redis_mock)


def _test_redis_erm_create_with_no_name(redis_erm):
    with pytest.raises(RuntimeError):
        RedisErm(redis_erm)


def _test_redis_sccs_create_with_no_name(redis_erm):
    with pytest.raises(RuntimeError):
        RedisSccs(redis_erm)


def test_erm_get(redis_erm):
    redis_erm._storage.hget.return_value = '1.0'
    assert redis_erm.get(('A', 'B')) == 1.0


def test_iter_erm(redis_erm):
    redis_erm._storage.hkeys.return_value = [('USD', 'ABC'), ('ABC', 'ABC')]
    assert list(redis_erm) == [('USD', 'ABC'), ('ABC', 'ABC')]


def test_set_invalid_erm(redis_erm):
    with pytest.raises(ValueError):
        redis_erm[('U', 'R')] = 1


def test_set_valid_erm(redis_erm):
    redis_erm[('USD', 'RUB')] = 1

def test_sccs_add_invalid(redis_sccs):
    with pytest.raises(ValueError):
        redis_sccs.add('a')


def test_sccs_add_valid(redis_sccs):
    redis_sccs.add('USD')


def test_sccs_contains(redis_sccs):
    redis_sccs._storage.sismember.return_value = True
    assert 'a' in redis_sccs


def test_sccs_mcontains_all(redis_sccs):
    redis_sccs._storage.smismember.return_value = [1,1]
    assert all(redis_sccs.mcontains(['a', 'b']))


def test_sccs_mcontains_any(redis_sccs):
    redis_sccs._storage.smismember.return_value = [1, 0]
    assert any(redis_sccs.mcontains(['a', 'b']))


def test_sccs_mcontains_none(redis_sccs):
    redis_sccs._storage.smismember.return_value = [0, 0]
    assert not all(redis_sccs.mcontains(['a', 'b']))
