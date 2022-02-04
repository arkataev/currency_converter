from celery import Task

from .data_structures import PersistentErm
from .storage import MemStorage


class ErmStorageRefreshTask(Task):
    erm: PersistentErm = PersistentErm(MemStorage()) # TODO:: will be using Redis storage here

    def run(self, cc_pair, **kwargs):
        # TODO: fetch url
        pass

    def on_success(self, retval, task_id, cc_pair, kwargs):
        self.erm[cc_pair] = retval
