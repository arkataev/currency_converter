from flask.views import View

from currency_exchanger.currency_converter import CConfig, CurrencyConverter
from currency_exchanger.data_structures import PersistentErm
from currency_exchanger.storage import MemStorage


class ExchangeAPI(View):
    config: CConfig = CConfig(erm=PersistentErm(MemStorage()))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.converter = CurrencyConverter(self.config)

    def exchange_view(self, code_x, code_y, amount):
        result = self.converter.exchange(code_x, code_y, amount)
        return result
