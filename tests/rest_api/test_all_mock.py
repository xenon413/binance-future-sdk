import pytest
from unittest.mock import patch
from decimal import Decimal

from binance_future_sdk.core.rest_api import (
    get_server_time, get_exchange_info, get_cont_kline, get_order_book_ticker,
    get_symbol_price_ticker, new_order, cancel_order, query_order, modify_order,
    change_margin_type, change_position_mode, change_leverage, change_multi_assets_mode,
    get_account_balance, get_account_config, get_symbol_config, cancel_all_order,
    auto_cancel_order, get_position_info
)
from binance_future_sdk.core.rest_api.const import (
    CandleInterval, ContractType, OrderSide, OrderType, PositionSide,
    TimeInForce, MarginType, PriceMatch
)
import binance_future_sdk.core.rest_api.request as request_module

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code
        self.text = "mock test"
    
    def json(self):
        return self.json_data

def test_get_server_time_mock(mocker):
    mocker.patch("requests.request", return_value=MockResponse({"serverTime": 123456789}))
    res = get_server_time(test=True)
    assert res.server_time == 123456789

def test_get_exchange_info_mock(mocker):
    mock_data = {
        "timezone": "UTC", "serverTime": 123456789, "futuresType": "U_MARGINED",
        "rateLimits": [], "assets": [], "symbols": [], "exchangeFilters": []
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_exchange_info(test=True)
    assert res.timezone == "UTC"

def test_get_cont_kline_mock(mocker):
    mocker.patch("requests.request", return_value=MockResponse([]))
    res = get_cont_kline(pair="BTCUSDT", interval=CandleInterval.MIN_1, contractType=ContractType.PERPETUAL, test=True)
    assert len(res.root) == 0

def test_get_order_book_ticker_mock(mocker):
    mock_data = {
        "symbol": "BTCUSDT", "bidPrice": "100", "bidQty": "1",
        "askPrice": "101", "askQty": "1", "time": 123
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_order_book_ticker(symbol="BTCUSDT", test=True)
    assert res.symbol == "BTCUSDT"

def test_get_symbol_price_ticker_mock(mocker):
    mock_data = {"symbol": "BTCUSDT", "price": "10000", "time": 123}
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_symbol_price_ticker(symbol="BTCUSDT", test=True)
    assert res.symbol == "BTCUSDT"

# Mock for secure endpoints
def test_new_order_mock(mocker, api_credentials):
    mock_data = {
        "clientOrderId": "test", "cumQty": "0", "cumQuote": "0", "executedQty": "0",
        "orderId": 123, "avgPrice": "0", "origQty": "1", "price": "10000", "reduceOnly": False,
        "side": "BUY", "positionSide": "BOTH", "status": "NEW", "stopPrice": "0",
        "closePosition": False, "symbol": "BTCUSDT", "timeInForce": "GTC", "type": "LIMIT",
        "origType": "LIMIT", "updateTime": 123, "workingType": "CONTRACT_PRICE", "priceProtect": False,
        "priceMatch": "NONE", "selfTradePreventionMode": "NONE", "goodTillDate": 0
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = new_order(**api_credentials, symbol="BTCUSDT", side=OrderSide.BUY, type=OrderType.LIMIT, quantity=Decimal("1"), price=Decimal("10000"), test=True)
    assert res.order_id == 123

def test_cancel_order_mock(mocker, api_credentials):
    mock_data = {
        "clientOrderId": "test", "cumQty": "0", "cumQuote": "0", "executedQty": "0",
        "orderId": 123, "origQty": "1", "origType": "LIMIT", "price": "10000", "avgPrice": "0",
        "reduceOnly": False, "side": "BUY", "positionSide": "BOTH", "status": "CANCELED",
        "stopPrice": "0", "closePosition": False, "symbol": "BTCUSDT", "timeInForce": "GTC",
        "type": "LIMIT", "updateTime": 123, "workingType": "CONTRACT_PRICE", "priceProtect": False,
        "priceMatch": "NONE", "selfTradePreventionMode": "NONE", "goodTillDate": 0
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = cancel_order(**api_credentials, symbol="BTCUSDT", orderId=123, test=True)
    assert res.order_id == 123

def test_query_order_mock(mocker, api_credentials):
    mock_data = {
        "avgPrice": "0", "clientOrderId": "test", "cumQuote": "0", "executedQty": "0",
        "orderId": 123, "origQty": "1", "origType": "LIMIT", "price": "10000", "reduceOnly": False,
        "side": "BUY", "positionSide": "BOTH", "status": "NEW", "stopPrice": "0",
        "closePosition": False, "symbol": "BTCUSDT", "time": 123, "timeInForce": "GTC",
        "type": "LIMIT", "updateTime": 123, "workingType": "CONTRACT_PRICE", "priceProtect": False,
        "priceMatch": "NONE", "selfTradePreventionMode": "NONE", "goodTillDate": 0
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = query_order(**api_credentials, symbol="BTCUSDT", orderId=123, test=True)
    assert res.order_id == 123

def test_modify_order_mock(mocker, api_credentials):
    mock_data = {
        "orderId": 123, "symbol": "BTCUSDT", "status": "NEW", "clientOrderId": "test",
        "price": "10000", "avgPrice": "0", "origQty": "1", "executedQty": "0", "cumQty": "0",
        "cumQuote": "0", "timeInForce": "GTC", "type": "LIMIT", "reduceOnly": False,
        "closePosition": False, "side": "BUY", "positionSide": "BOTH", "stopPrice": "0",
        "workingType": "CONTRACT_PRICE", "priceProtect": False, "origType": "LIMIT",
        "priceMatch": "NONE", "selfTradePreventionMode": "NONE", "goodTillDate": 0, "updateTime": 123
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = modify_order(**api_credentials, symbol="BTCUSDT", side=OrderSide.BUY, quantity=Decimal("2"), orderId=123, test=True)
    assert res.order_id == 123


def test_change_margin_type_mock(mocker, api_credentials):
    mocker.patch("requests.request", return_value=MockResponse({"code": 200, "msg": "success"}))
    res = change_margin_type(**api_credentials, symbol="BTCUSDT", margintype=MarginType.ISOLATED, test=True)
    assert res.code == 200

def test_change_position_mode_mock(mocker, api_credentials):
    mocker.patch("requests.request", return_value=MockResponse({"code": 200, "msg": "success"}))
    res = change_position_mode(**api_credentials, dualSidePosition=True, test=True)
    assert res.code == 200

def test_change_leverage_mock(mocker, api_credentials):
    mock_data = {"leverage": 20, "maxNotionalValue": "1000000", "symbol": "BTCUSDT"}
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = change_leverage(**api_credentials, symbol="BTCUSDT", leverage=20, test=True)
    assert res.leverage == 20

def test_change_multi_assets_mode_mock(mocker, api_credentials):
    mocker.patch("requests.request", return_value=MockResponse({"code": 200, "msg": "success"}))
    res = change_multi_assets_mode(**api_credentials, multiAssetsMargin=True, test=True)
    assert res.code == 200

def test_get_account_balance_mock(mocker, api_credentials):
    mocker.patch("requests.request", return_value=MockResponse([]))
    res = get_account_balance(**api_credentials, test=True)
    assert len(res.root) == 0

def test_get_account_config_mock(mocker, api_credentials):
    mock_data = {
        "feeTier": 0, "canTrade": True, "canDeposit": True, "canWithdraw": True,
        "dualSidePosition": False, "updateTime": 123, "multiAssetsMargin": False, "tradeGroupId": 0
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_account_config(**api_credentials, test=True)
    assert res.can_trade == True

def test_get_symbol_config_mock(mocker, api_credentials):
    mocker.patch("requests.request", return_value=MockResponse([]))
    res = get_symbol_config(**api_credentials, symbol=False, test=True)
    assert len(res.root) == 0

def test_cancel_all_order_mock(mocker, api_credentials):
    mocker.patch("requests.request", return_value=MockResponse({"code": 200, "msg": "success"}))
    res = cancel_all_order(**api_credentials, symbol="BTCUSDT", test=True)
    assert res.code == 200

def test_auto_cancel_order_mock(mocker, api_credentials):
    mock_data = {"symbol": "BTCUSDT", "countdownTime": "10000"}
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = auto_cancel_order(**api_credentials, symbol="BTCUSDT", countdownTime=10000, test=True)
    assert res.symbol == "BTCUSDT"

def test_get_position_info_mock(mocker, api_credentials):
    mocker.patch("requests.request", return_value=MockResponse([]))
    res = get_position_info(**api_credentials, Symbol="BTCUSDT", test=True)
    assert len(res.root) == 0
