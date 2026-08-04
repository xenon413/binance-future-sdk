import pytest
from unittest.mock import patch
from decimal import Decimal

from binance_future_sdk.rest_api import (
    get_server_time, get_exchange_info, get_cont_kline, get_order_book_ticker,
    get_symbol_price_ticker, new_order, cancel_order, query_order, modify_order,
    change_margin_type, change_position_mode, change_leverage, change_multi_assets_mode,
    get_account_balance, get_account_config, get_symbol_config, cancel_all_order,
    auto_cancel_order, get_position_info,
    CandleInterval, ContractType, OrderSide, OrderType, PositionSide,
    TimeInForce, MarginType, PriceMatch
)

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code
        self.text = "mock test"
    
    def json(self):
        return self.json_data

def test_get_server_time_mock(mocker):
    mocker.patch("requests.request", return_value=MockResponse({"serverTime": 1499827319559}))
    res = get_server_time(test=True)
    assert res.server_time == 1499827319559

def test_get_exchange_info_mock(mocker):
    mock_data = {
        "timezone": "UTC", "serverTime": 123456789, "futuresType": "U_MARGINED",
        "rateLimits": [], "assets": [], "symbols": [], "exchangeFilters": []
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_exchange_info(test=True)
    assert res.timezone == "UTC"

def test_get_cont_kline_mock(mocker):
    mock_data = [
        [
            1607444700000,
            "18879.99",
            "18900.00",
            "18878.98",
            "18896.13",
            "492.363",
            1607444759999,
            "9302145.66080",
            1874,
            "385.983",
            "7292402.33267",
            "0"
        ],
    ]
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_cont_kline(pair="BTCUSDT", interval=CandleInterval.MIN_1, contractType=ContractType.PERPETUAL, test=True)
    assert len(res.root) == 1
    assert res.df.shape == (1, 12)
    assert res.df.loc[0, "open_price"] == Decimal("18879.99")

def test_get_order_book_ticker_mock(mocker):
    mock_data = {
        "symbol": "BTCUSDT",
        "bidPrice": "4.00000000",
        "bidQty": "431.00000000",
        "askPrice": "4.00000200",
        "askQty": "9.00000000",
        "time": 1589437530011
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_order_book_ticker(symbol="BTCUSDT", test=True)
    assert res.symbol == "BTCUSDT"

def test_get_symbol_price_ticker_mock(mocker):
    mock_data = {
        "symbol": "BTCUSDT",
        "price": "6000.01",
        "time": 1589437530011
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_symbol_price_ticker(symbol="BTCUSDT", test=True)
    assert res.symbol == "BTCUSDT"

# Mock for secure endpoints
def test_new_order_mock(mocker, api_credentials):
    mock_data = {
        "clientOrderId": "testOrder",
        "cumQty": "0",
        "executedQty": "0",
        "orderId": 22542179,
        "origQty": "10",
        "price": "0",
        "reduceOnly": False,
        "side": "SELL",
        "positionSide": "SHORT",
        "status": "NEW",
        "stopPrice": "0",
        "closePosition": False,
        "symbol": "BTCUSDT",
        "timeInForce": "GTD",
        "type": "LIMIT",
        "origType": "LIMIT",
        "updateTime": 1566818724722,
        "workingType": "CONTRACT_PRICE",
        "priceProtect": False,
        "priceMatch": "NONE",
        "selfTradePreventionMode": "NONE",
        "goodTillDate": 1693207680000
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = new_order(**api_credentials, symbol="BTCUSDT", side=OrderSide.BUY, type=OrderType.LIMIT, quantity=Decimal("1"), price=Decimal("10000"), test=True)
    assert res.order_id == 22542179

def test_cancel_order_mock(mocker, api_credentials):
    mock_data = {
        "clientOrderId": "myOrder1",
        "cumQty": "0",
        "executedQty": "0",
        "orderId": 283194212,
        "origQty": "11",
        "price": "0",
        "reduceOnly": False,
        "side": "BUY",
        "positionSide": "SHORT",
        "status": "CANCELED",
        "stopPrice": "9300",
        "closePosition": False,
        "symbol": "BTCUSDT",
        "timeInForce": "GTC",
        "origType": "TRAILING_STOP_MARKET",
        "type": "TRAILING_STOP_MARKET",
        "activatePrice": "9020",
        "priceRate": "0.3",
        "updateTime": 1571110484038,
        "workingType": "CONTRACT_PRICE",
        "priceProtect": False,
        "priceMatch": "NONE",
        "selfTradePreventionMode": "NONE",
        "goodTillDate": 0
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = cancel_order(**api_credentials, symbol="BTCUSDT", orderId=283194212, test=True)
    assert res.order_id == 283194212

def test_query_order_mock(mocker, api_credentials):
    mock_data = {
        "avgPrice": "0.00000",
        "clientOrderId": "abc",
        "cumQuote": "0",
        "executedQty": "0",
        "orderId": 1573346959,
        "origQty": "0.40",
        "origType": "TRAILING_STOP_MARKET",
        "price": "0",
        "reduceOnly": False,
        "side": "BUY",
        "positionSide": "SHORT",
        "status": "NEW",
        "stopPrice": "9300",
        "closePosition": False,
        "symbol": "BTCUSDT",
        "time": 1579276756075,
        "timeInForce": "GTC",
        "type": "TRAILING_STOP_MARKET",
        "activatePrice": "9020",
        "priceRate": "0.3",
        "updateTime": 1579276756075,
        "workingType": "CONTRACT_PRICE",
        "priceProtect": False,
        "priceMatch": "NONE",
        "selfTradePreventionMode": "NONE",
        "goodTillDate": 0
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = query_order(**api_credentials, symbol="BTCUSDT", orderId=1573346959, test=True)
    assert res.order_id == 1573346959

def test_modify_order_mock(mocker, api_credentials):
    mock_data = {
        "orderId": 20072994037,
        "symbol": "BTCUSDT",
        "pair": "BTCUSDT",
        "status": "NEW",
        "clientOrderId": "LJ9R4QZDihCaS8UAOOLpgW",
        "modifyId": 1,
        "price": "30005",
        "origQty": "1",
        "executedQty": "0",
        "cumQty": "0",
        "timeInForce": "GTC",
        "type": "LIMIT",
        "reduceOnly": True,
        "closePosition": True,
        "side": "BUY",
        "positionSide": "LONG",
        "stopPrice": "0",
        "workingType": "CONTRACT_PRICE",
        "priceProtect": True,
        "origType": "LIMIT",
        "priceMatch": "NONE",
        "selfTradePreventionMode": "NONE",
        "goodTillDate": 0,
        "updateTime": 1629182711600
    }
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = modify_order(**api_credentials, symbol="BTCUSDT", side=OrderSide.BUY, quantity=Decimal("1.0"), orderId=20072994037, price=Decimal("30005"), test=True)
    assert res.order_id == 20072994037

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
    mock_data = [
        {
            "accountAlias":"uX",
            "asset":"FDUSD",
            "balance":"0.00000000",
            "crossWalletBalance":"0.00000000",
            "crossUnPnl":"0.00000000",
            "availableBalance":"0.00000000",
            "maxWithdrawAmount":"0.00000000",
            "marginAvailable":True,
            "updateTime":0
        },
        {
            "accountAlias":"uX",
            "asset":"U",
            "balance":"0.00000000",
            "crossWalletBalance":"0.00000000",
            "crossUnPnl":"0.00000000",
            "availableBalance":"0.00000000",
            "maxWithdrawAmount":"0.00000000",
            "marginAvailable":True,
            "updateTime":0
        },
    ]
    mocker.patch("requests.request", return_value=MockResponse(mock_data))
    res = get_account_balance(**api_credentials, test=True)
    assert len(res.root) == 2

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
