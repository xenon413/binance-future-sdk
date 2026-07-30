from typing import Optional
from decimal import Decimal

from .const import (
    CandleInterval,
    ContractType,
    MarginType,
    OrderSide,
    OrderType,
    PositionSide,
    PriceMatch,
    TimeInForce
)
from .request import request
from .schema import (
    RestEndpointCollection,
    ServerTimeKwargs, ServerTimeReturn,
    ExchangeInfoKwargs, ExchangeInfoReturn,
    ContKlineKwargs, ContKlineReturn,
    OrderBookTickerKwargs, OrderBookTickerReturn,
    SymbolPriceTickerKwargs, SymbolPriceTickerReturn,
    NewOrderKwargs, NewOrderReturn,
    CancelOrderKwargs, CancelOrderReturn,
    QueryOrderKwargs, QueryOrderReturn,
    ModifyOrderKwargs, ModifyOrderReturn,
    ChangeMarginTypeKwargs, ChangeMarginTypeReturn,
    ChangePositionModeKwargs, ChangePositionModeReturn,
    ChangeLeverageKwargs, ChangeLeverageReturn,
    ChangeMultiAssetsModeKwargs, ChangeMultiAssetsModeReturn,
    AccountBalanceKwargs, AccountBalanceReturn,
    AccountConfigKwargs, AccountConfigReturn,
    SymbolConfigKwargs, SymbolConfigReturn,
    CancelAllOrderKwargs, CancelAllOrderReturn,
    AutoCancelOrderKwargs, AutoCancelOrderReturn,
    PositionInfoKwargs, PositionInfoReturn
)

def get_server_time(test: bool = False) -> ServerTimeReturn:
    """Get the current server time."""
    kwargs = ServerTimeKwargs()
    return request(RestEndpointCollection.SERVER_TIME.value, kwargs, test)

def get_exchange_info(test: bool = False) -> ExchangeInfoReturn:
    """Get current exchange trading rules and symbol information."""
    kwargs = ExchangeInfoKwargs()
    return request(RestEndpointCollection.EXCHANGE_INFO.value, kwargs, test)

def get_cont_kline(
    pair: str,
    interval: CandleInterval,
    contractType: ContractType,
    startTime: Optional[int] = None,
    endTime: Optional[int] = None,
    limit: Optional[int] = None,
    test: bool = False
) -> ContKlineReturn:
    """Get continuous kline data."""
    kwargs = ContKlineKwargs(
        pair=pair, interval=interval, contractType=contractType,
        startTime=startTime, endTime=endTime, limit=limit
    )
    return request(RestEndpointCollection.CONT_KLINE.value, kwargs, test)

def get_order_book_ticker(symbol: str, test: bool = False) -> OrderBookTickerReturn:
    """Get best price/qty on the order book for a symbol or symbols."""
    kwargs = OrderBookTickerKwargs(symbol=symbol)
    return request(RestEndpointCollection.ORDER_BOOK_TICKER.value, kwargs, test)

def get_symbol_price_ticker(symbol: str, test: bool = False) -> SymbolPriceTickerReturn:
    """Get the latest price for a symbol or symbols."""
    kwargs = SymbolPriceTickerKwargs(symbol=symbol)
    return request(RestEndpointCollection.SYMBOL_PRICE_TICKER.value, kwargs, test)

def new_order(
    key: str,
    secret: str,
    symbol: str,
    side: OrderSide,
    type: OrderType,
    positionSide: Optional[PositionSide] = None,
    timeInForce: Optional[TimeInForce] = None,
    quantity: Optional[Decimal] = None,
    reduceOnly: Optional[str] = None,
    price: Optional[Decimal] = None,
    newClientOrderId: Optional[str] = None,
    newOrderRespType: Optional[str] = None,
    priceMatch: Optional[PriceMatch] = None,
    selfTradePreventionMode: Optional[str] = None,
    goodTillDate: Optional[int] = None,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> NewOrderReturn:
    """Send in a new order."""
    kwargs = NewOrderKwargs(
        key=key, secret=secret, symbol=symbol, side=side, type=type,
        positionSide=positionSide, timeInForce=timeInForce, quantity=quantity,
        reduceOnly=reduceOnly, price=price, newClientOrderId=newClientOrderId,
        newOrderRespType=newOrderRespType, priceMatch=priceMatch,
        selfTradePreventionMode=selfTradePreventionMode, goodTillDate=goodTillDate,
        recv_window=recv_window
    )
    return request(RestEndpointCollection.NEW_ORDER.value, kwargs, test)

def cancel_order(
    key: str,
    secret: str,
    symbol: str,
    orderId: Optional[int] = None,
    origClientOrderId: Optional[str] = None,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> CancelOrderReturn:
    """Cancel an active order."""
    kwargs = CancelOrderKwargs(
        key=key, secret=secret, symbol=symbol, orderId=orderId, 
        origClientOrderId=origClientOrderId, recv_window=recv_window
    )
    return request(RestEndpointCollection.CANCEL_ORDER.value, kwargs, test)

def query_order(
    key: str,
    secret: str,
    symbol: str,
    orderId: Optional[int] = None,
    origClientOrderId: Optional[str] = None,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> QueryOrderReturn:
    """Check an order's status."""
    kwargs = QueryOrderKwargs(
        key=key, secret=secret, symbol=symbol, orderId=orderId, 
        origClientOrderId=origClientOrderId, recv_window=recv_window
    )
    return request(RestEndpointCollection.QUERY_ORDER.value, kwargs, test)

def modify_order(
    key: str,
    secret: str,
    symbol: str,
    side: OrderSide,
    quantity: Decimal,
    orderId: Optional[int] = None,
    origClientOrderId: Optional[str] = None,
    price: Optional[Decimal] = None,
    priceMatch: Optional[PriceMatch] = None,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> ModifyOrderReturn:
    """Modify an active order."""
    kwargs = ModifyOrderKwargs(
        key=key, secret=secret, symbol=symbol, side=side, quantity=quantity,
        orderId=orderId, origClientOrderId=origClientOrderId, price=price,
        priceMatch=priceMatch, recv_window=recv_window
    )
    return request(RestEndpointCollection.MODIFY_ORDER.value, kwargs, test)

def change_margin_type(
    key: str,
    secret: str,
    symbol: str,
    margintype: MarginType,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> ChangeMarginTypeReturn:
    """Change user's margin type in the specified symbol market."""
    kwargs = ChangeMarginTypeKwargs(
        key=key, secret=secret, symbol=symbol, margintype=margintype,
        recv_window=recv_window
    )
    return request(RestEndpointCollection.CHANGE_MARGIN_TYPE.value, kwargs, test)

def change_position_mode(
    key: str,
    secret: str,
    dualSidePosition: bool,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> ChangePositionModeReturn:
    """Change user's position mode (Hedge Mode or One-way Mode)."""
    kwargs = ChangePositionModeKwargs(
        key=key, secret=secret, dualSidePosition=dualSidePosition,
        recv_window=recv_window
    )
    return request(RestEndpointCollection.CHANGE_POSITION_MODE.value, kwargs, test)

def change_leverage(
    key: str,
    secret: str,
    symbol: str,
    leverage: int,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> ChangeLeverageReturn:
    """Change user's initial leverage of specific symbol market."""
    kwargs = ChangeLeverageKwargs(
        key=key, secret=secret, symbol=symbol, leverage=leverage,
        recv_window=recv_window
    )
    return request(RestEndpointCollection.CHANGE_LEVERAGE.value, kwargs, test)

def change_multi_assets_mode(
    key: str,
    secret: str,
    multiAssetsMargin: bool,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> ChangeMultiAssetsModeReturn:
    """Change user's Multi-Assets mode."""
    kwargs = ChangeMultiAssetsModeKwargs(
        key=key, secret=secret, multiAssetsMargin=multiAssetsMargin,
        recv_window=recv_window
    )
    return request(RestEndpointCollection.CHANGE_MULTI_ASSETS_MODE.value, kwargs, test)

def get_account_balance(
    key: str,
    secret: str,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> AccountBalanceReturn:
    """Get user's account balance."""
    kwargs = AccountBalanceKwargs(key=key, secret=secret, recv_window=recv_window)
    return request(RestEndpointCollection.ACCOUNT_BALANCE.value, kwargs, test)

def get_account_config(
    key: str,
    secret: str,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> AccountConfigReturn:
    """Get user's account configuration."""
    kwargs = AccountConfigKwargs(key=key, secret=secret, recv_window=recv_window)
    return request(RestEndpointCollection.ACCOUNT_CONFIG.value, kwargs, test)

def get_symbol_config(
    key: str,
    secret: str,
    symbol: bool,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> SymbolConfigReturn:
    """Get user's symbol configuration."""
    kwargs = SymbolConfigKwargs(
        key=key, secret=secret, symbol=symbol, recv_window=recv_window
    )
    return request(RestEndpointCollection.SYMBOL_CONFIG.value, kwargs, test)

def cancel_all_order(
    key: str,
    secret: str,
    symbol: str,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> CancelAllOrderReturn:
    """Cancel all active orders on a symbol."""
    kwargs = CancelAllOrderKwargs(
        key=key, secret=secret, symbol=symbol, recv_window=recv_window
    )
    return request(RestEndpointCollection.CANCEL_ALL_ORDER.value, kwargs, test)

def auto_cancel_order(
    key: str,
    secret: str,
    symbol: str,
    countdownTime: int,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> AutoCancelOrderReturn:
    """Auto-cancel all active orders on a symbol."""
    kwargs = AutoCancelOrderKwargs(
        key=key, secret=secret, symbol=symbol, countdownTime=countdownTime,
        recv_window=recv_window
    )
    return request(RestEndpointCollection.AUTO_CANCEL_ORDER.value, kwargs, test)

def get_position_info(
    key: str,
    secret: str,
    Symbol: str,
    recv_window: Optional[int] = 5000,
    test: bool = False
) -> PositionInfoReturn:
    """Get current position information."""
    kwargs = PositionInfoKwargs(
        key=key, secret=secret, Symbol=Symbol, recv_window=recv_window
    )
    return request(RestEndpointCollection.POSITION_INFO.value, kwargs, test)
