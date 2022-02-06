from itertools import permutations

from celery import Task, Celery, group
from celery.utils.log import get_task_logger
from redis import Redis
from requests import Timeout

from .cer_providers import FreeCurrencyRateProvider
from .data_structures import RedisErm, RedisSccs

__all__ = ['refresh_erm', 'refresh_currency']

app = Celery('tasks', broker='amqp://localhost')
redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)
logger = get_task_logger(__name__)


class RefreshCurrencyTask(Task):
    name = 'refresh_currency'
    ignore_result = True
    max_retries = 10

    def __init__(self, _redis):
        self._erm = RedisErm(_redis)
        self._provider = FreeCurrencyRateProvider()

    def run(self, base_ccode: str, target_ccode: str, **kwargs):
        logger.info(f'Fetching exchange rate for {base_ccode, target_ccode}')
        try:
            cer = self._provider.fetch_cer(base_ccode, target_ccode)
        except Timeout as e:
            logger.warning(f'Timeout fetching exchange rate for {base_ccode, target_ccode}')
            raise self.retry(exc=e)
        return cer

    def on_success(self, retval, task_id, cc_pair, kwargs):
        if not retval:
            logger.warning(f'No exchange rate for currencies {cc_pair}')
            return
        logger.info(f'Successfully fetched exchange rate for currencies {cc_pair}')
        self._erm[cc_pair] = retval

    def on_failure(self, exc, task_id, cc_pair, kwargs, einfo):
        logger.warning(f'Failed to update exchange rate for currencies{cc_pair}. Error: {exc}')


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
