import time
from itertools import permutations

from celery import Task, Celery, group
from redis import Redis

from .data_structures import RedisErm, RedisSccs

__all__ = ['refresh_erm', 'refresh_currency']


app = Celery('tasks', broker='amqp://localhost')
redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)


class RefreshCurrencyTask(Task):
    name = 'refresh_currency'
    ignore_result = True

    def __init__(self, _redis):
        self._erm = RedisErm(_redis)

    def run(self, *args, **kwargs):
        # TODO:: Fetch exchange rate for currencies pair
        time.sleep(2) # TODO: remove
        print(f'Updated {args}')
        return 1

    def on_success(self, retval, task_id, cc_pair, kwargs):
        self._erm[cc_pair] = retval


refresh_currency = app.register_task(RefreshCurrencyTask(redis))


class RefreshErmTask(Task):
    name = 'refresh_erm'
    ignore_result = True

    def __init__(self, _redis):
        self._sccs = RedisSccs(_redis)

    def run(self, *args, **kwargs):
        supported_currencies = permutations(self._sccs, 2)
        group(refresh_currency.s(*pair) for pair in supported_currencies).apply_async()


refresh_erm = app.register_task(RefreshErmTask(redis))
