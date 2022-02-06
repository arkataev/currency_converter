import pytest
import responses

from currency_exchanger.cer_providers import FreeCurrencyRateProvider, CerResourceError


class TestFreeCurrencyRateProvider:

    @pytest.fixture
    def provider(self):
        return FreeCurrencyRateProvider()

    @responses.activate
    def test_provider_success(self, provider):
        responses.add(
            responses.GET,
            url=provider.api,
            json={'data': {'rub': 1}},
            status=200,
        )
        resp = provider.fetch_cer('usd', 'rub')
        assert resp == 1

    @responses.activate
    def test_provider_unexpected_response(self, provider):
        responses.add(
            responses.GET,
            url=provider.api,
            status=200,
        )
        with pytest.raises(CerResourceError):
            provider.fetch_cer('usd', 'rub')

    @responses.activate
    def test_provider_failed(self, provider):
        responses.add(
            responses.GET,
            url=provider.api,
            json={'error': 'message'},
            status=400,
        )
        with pytest.raises(CerResourceError):
            provider.fetch_cer('usd', 'rub')

    @responses.activate
    def test_provider_no_data(self, provider):
        responses.add(
            responses.GET,
            url=provider.api,
            json={'error': 'message'},
            status=200,
        )
        with pytest.raises(CerResourceError):
            provider.fetch_cer('usd', 'rub')

