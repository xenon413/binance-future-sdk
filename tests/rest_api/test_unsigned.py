import pytest

from binance_future_sdk.rest_api import (
    get_server_time, get_exchange_info, get_cont_kline, get_order_book_ticker,
    get_symbol_price_ticker, CandleInterval, ContractType
)

@pytest.mark.integration
def test_get_server_time():
    res = get_server_time()
    assert res.server_time > 0

@pytest.mark.integration
def test_get_cont_kline():
    res = get_cont_kline(
        pair="BTCUSDC",
        contractType=ContractType.PERPETUAL,
        interval=CandleInterval.MIN_1,
    )
    assert len(res.root) == 500
    assert res.df.shape == (500, 12)

@pytest.mark.integration
def test_get_exchange_info():
    res = get_exchange_info()

@pytest.mark.integration
def test_get_order_book_ticker():
    res = get_order_book_ticker("BTCUSDC")

@pytest.mark.integration
def test_get_symbol_price_ticker():
    res = get_symbol_price_ticker("BTCUSDC")

