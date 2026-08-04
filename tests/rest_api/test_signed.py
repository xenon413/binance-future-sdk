import pytest

from binance_future_sdk.rest_api import (
    new_order, cancel_order, query_order, modify_order,
    change_margin_type, change_position_mode, change_leverage, change_multi_assets_mode,
    get_account_balance, get_account_config, get_symbol_config, cancel_all_order,
    auto_cancel_order, get_position_info,
    CandleInterval, ContractType, OrderSide, OrderType, PositionSide,
    TimeInForce, MarginType, PriceMatch
)

@pytest.mark.integration
def test_get_account_balance(api_credentials):
    res = get_account_balance(**api_credentials, test=True)

@pytest.mark.integration
def test_get_account_config(api_credentials):
    res = get_account_config(**api_credentials, test=True)

@pytest.mark.integration
def test_get_symbol_config(api_credentials):
    res = get_symbol_config(**api_credentials, symbol="BTCUSDT", test=True)

@pytest.mark.integration
def test_get_position_info(api_credentials):
    res = get_position_info(**api_credentials, symbol="BTCUSDT", test=True)


