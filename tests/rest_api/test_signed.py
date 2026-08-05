import pytest
from decimal import Decimal

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


@pytest.mark.integration
def test_change_margin_settings(api_credentials):
    ### currently assume that initial margin type is isolated
    # because multi assets could only be set when crossed margin to the test proccess is:
    # to cross position -> multi assets -> single assets -> isolate position
    # note: to change multi asset you'll need all assets to be in crossed, currently only have USDC
    # change_margin_type(**api_credentials, symbol="BTCUSDC", margintype=MarginType.ISOLATED, test=True)
    change_margin_type(**api_credentials, symbol="BTCUSDC", margintype=MarginType.CROSSED, test=True)

    change_multi_assets_mode(**api_credentials, multiAssetsMargin=True, test=True)
    change_multi_assets_mode(**api_credentials, multiAssetsMargin=False, test=True)

    change_margin_type(**api_credentials, symbol="BTCUSDC", margintype=MarginType.ISOLATED, test=True)

@pytest.mark.integration
def test_change_position_mode(api_credentials):
    ### assume that initial position mode is on dual
    change_position_mode(**api_credentials, dualSidePosition=False, test=True)
    change_position_mode(**api_credentials, dualSidePosition=True, test=True)

@pytest.mark.integration
def test_change_leverage(api_credentials):
    change_leverage(**api_credentials, symbol="BTCUSDC", leverage=10, test=True)
    change_leverage(**api_credentials, symbol="BTCUSDC", leverage=1, test=True)

@pytest.mark.integration
def test_order_lifecycle1(api_credentials):
    # lifecycle: limit order -> query -> cancel -> query
    # creating new limit order queue_20 so it stays on the book
    res = new_order(
        **api_credentials,
        symbol="BTCUSDC",
        priceMatch=PriceMatch.QUEUE_20,
        quantity=Decimal("0.005"),
        side=OrderSide.BUY,
        positionSide=PositionSide.LONG,
        timeInForce=TimeInForce.GTX,
        type=OrderType.LIMIT,
        test=True
    )

    # query after order placed
    res = query_order(
        **api_credentials,
        orderId=res.order_id,
        symbol=res.symbol,
        test=True
    )

    res = cancel_order(
        **api_credentials,
        orderId=res.order_id,
        symbol=res.symbol,
        test=True
    )

    # query when no order
    res = query_order(
        **api_credentials,
        orderId=res.order_id,
        symbol=res.symbol,
        test=True
    )

@pytest.mark.integration
def test_order_lifecycle2(api_credentials):
    # lifecycle: limit order -> modify*2 -> auto cancel
    res = new_order(
        **api_credentials,
        symbol="BTCUSDC",
        priceMatch=PriceMatch.QUEUE_20,
        quantity=Decimal("0.005"),
        side=OrderSide.BUY,
        positionSide=PositionSide.LONG,
        timeInForce=TimeInForce.GTX,
        type=OrderType.LIMIT,
        test=True
    )

    res = modify_order(
        **api_credentials,
        orderId=res.order_id,
        symbol="BTCUSDC",
        side=OrderSide.BUY,
        price=res.price,
        quantity=Decimal("0.006"),
        test=True
    )

    res = modify_order(
        **api_credentials,
        orderId=res.order_id,
        symbol="BTCUSDC",
        side=OrderSide.BUY,
        priceMatch=PriceMatch.QUEUE_20,
        quantity=Decimal("0.007"),
        test=True
    )

    res = auto_cancel_order(
        **api_credentials,
        symbol="BTCUSDC",
        countdownTime=1,
        test=True
    )

@pytest.mark.integration
def test_order_lifecycle3(api_credentials):
    # limit order -> cancel all
    cancel_all_order(
        **api_credentials,
        symbol="BTCUSDC",
        test=True
    )

    new_order(
        **api_credentials,
        symbol="BTCUSDC",
        priceMatch=PriceMatch.QUEUE_20,
        quantity=Decimal("0.005"),
        side=OrderSide.BUY,
        positionSide=PositionSide.LONG,
        timeInForce=TimeInForce.GTX,
        type=OrderType.LIMIT,
        test=True
    )

    cancel_all_order(
        **api_credentials,
        symbol="BTCUSDC",
        test=True
    )