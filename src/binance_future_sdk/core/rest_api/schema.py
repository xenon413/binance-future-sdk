from pydantic import BaseModel, ConfigDict, RootModel, Field,field_validator
import time
import hashlib
import hmac
from typing import Optional, TypeVar, Generic, Literal, ClassVar, Annotated, Union, List, Any, Type
from decimal import Decimal
import pandas as pd
from enum import Enum

from .const import(
    RequestMethod, 
    OrderSide, 
    PriceMatch, 
    CandleInterval,
    ContractType,
    PositionSide,
    OrderType,
    TimeInForce,
    MarginType,
    OrderStatus
)

class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
    )

class RequestConfig(MyBaseModel):
    ENDPOINT:ClassVar[str]
    METHOD:ClassVar[RequestMethod]
    RETURN_TYPE:ClassVar[Type[MyBaseModel|RootModel]]
    def query(self)->str:
        return "&".join([f"{k}={v}" for k, v in self.model_dump().items() if v is not None])

    def header(self)->dict:
        return {}
    
class SecureRequestConfig(RequestConfig):
    key:str
    secret:str
    recv_window:Optional[int]=5000

    def sign(self, query:str)->str:
        return hmac.new(
            self.secret.encode("utf-8"), 
            query.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()

    def timestamp(self, offset:int=0)->int:
        '''
        Params
            offset: in milliseconds
        '''
        return int(time.time()*1000) + offset
    
    def query(self, offset:int=0)->str:
        raw_query = "&".join([f"{k}={v}" for k, v in self.model_dump().items() if (v is not None) and (k not in ["key", "secret"])])
        raw_query += f"&{self.timestamp(offset)}"
        return self.sign(raw_query)

    def header(self)->dict:
        return {"X-MBX-APIKEY":self.key}

P = TypeVar("P", bound=RequestConfig) # Parameter Type
R = TypeVar("R", bound=MyBaseModel|RootModel) # Return Type

class ServerTimeReturn(MyBaseModel):
    server_time:int=Field(alias="serverTime")

class ServerTimeKwargs(RequestConfig):...

class _RateLimit(MyBaseModel):
    rate_limit_type:str=Field(alias="rateLimitType")
    interval:str
    interval_num:int=Field(alias="intervalNum")
    limit:int

class _Asset(MyBaseModel):
    asset:str
    margin_available:bool=Field(alias="marginAvailable")
    auto_asset_exchange:Decimal=Field(alias="autoAssetExchange")

class _PriceFilter(MyBaseModel):
    filter_type: Literal["PRICE_FILTER"] = Field(alias="filterType")
    min_price: Decimal = Field(alias="minPrice")
    max_price: Decimal = Field(alias="maxPrice")
    tick_size: Decimal = Field(alias="tickSize")
    
class _LotSizeFilter(MyBaseModel):
    filter_type: Literal["LOT_SIZE"] = Field(alias="filterType")
    min_qty: Decimal = Field(alias="minQty")
    max_qty: Decimal = Field(alias="maxQty")
    step_size: Decimal = Field(alias="stepSize")

class _MarketLotSizeFilter(MyBaseModel):
    filter_type: Literal["MARKET_LOT_SIZE"] = Field(alias="filterType")
    min_qty:Decimal = Field(alias="minQty")
    max_qty:Decimal = Field(alias="maxQty")
    step_size:Decimal = Field(alias="stepSize")

class _MaxNumOrderFilter(MyBaseModel):
    filter_type: Literal["MAX_NUM_ORDERS"] = Field(alias="filterType")
    limit:int

class _MaxNumAlgoOrderFilter(MyBaseModel):
    filter_type: Literal["MAX_NUM_ALGO_ORDERS"] = Field(alias="filterType")
    limit:int

class _MinNotionalFilter(MyBaseModel):
    filter_type: Literal["MIN_NOTIONAL"] = Field(alias="filterType")
    notional:Decimal

class _PercentPriceFilter(MyBaseModel):
    filter_type: Literal["PERCENT_PRICE"] = Field(alias="filterType")
    multiplier_up: Decimal = Field(alias="multiplierUp")
    multiplier_decimal:Decimal = Field(alias="multiplierDecimal")
    multiplier_down: Decimal = Field(alias="multiplierDown")

class _PositionRiskControlFilter(MyBaseModel):
    filter_type: Literal["POSITION_RISK_CONTROL"] = Field(alias="filterType")
    position_control_side:str = Field(alias="positionControlSide")

BinanceFilter = Annotated[
    Union[
        _PriceFilter, 
        _LotSizeFilter, 
        _MarketLotSizeFilter, 
        _MaxNumOrderFilter,
        _MaxNumAlgoOrderFilter,
        _MinNotionalFilter,  
        _PercentPriceFilter,
        _PositionRiskControlFilter
    ],
    Field(discriminator="filter_type") # This points to the field with Literal
]

class _Symbols(MyBaseModel):
    symbol:str
    pair:str
    contractType:ContractType
    deliveryDate:int
    onboardDate:int
    status:str
    maintMarginPercent:Decimal
    requiredMarginPercent:Decimal
    baseAsset:str
    quoteAsset:str
    marginAsset:str
    pricePrecision:int
    quantityPrecision:int
    baseAssetPrecision:int
    quotePrecision:int
    underlyingType:str
    underlyingSubType:list
    triggerProtect:Decimal
    liquidationFee:Decimal
    marketTakeBound:Decimal
    maxMoveOrderLimit:int
    filters:list[BinanceFilter]
    orderTypes:list[OrderType]
    timeInForce:list[TimeInForce]
    permissionSets:list

    @property
    def price_filter(self)->_PriceFilter|None:
        return next((f for f in self.filters if isinstance(f, _PriceFilter)), None)

    @property
    def lot_size(self)->_LotSizeFilter|None:
        return next((f for f in self.filters if isinstance(f, _LotSizeFilter)), None)

    @property
    def market_lot_size(self)->_MarketLotSizeFilter|None:
        return next((f for f in self.filters if isinstance(f, _MarketLotSizeFilter)), None)
    
    @property
    def max_num_order(self)->_MaxNumOrderFilter|None:
        return next((f for f in self.filters if isinstance(f, _MaxNumOrderFilter)), None)
    
    @property
    def max_num_algo_order(self)->_MaxNumAlgoOrderFilter|None:
        return next((f for f in self.filters if isinstance(f, _MaxNumAlgoOrderFilter)), None)

    @property
    def min_notional(self)->_MinNotionalFilter|None:
        return next((f for f in self.filters if isinstance(f, _MinNotionalFilter)), None)
    
    @property
    def percent_price_filter(self)->_PercentPriceFilter|None:
        return next((f for f in self.filters if isinstance(f, _PercentPriceFilter)), None)

    @property
    def Position_risk_control(self)->_PositionRiskControlFilter|None:
        return next((f for f in self.filters if isinstance(f, _PercentPriceFilter)), None)

class ExchangeInfoReturn(MyBaseModel):
    exchange_filter:list=Field(alias="exchangeFilters")
    timezone:str
    serverTime:int
    futuresType:str
    rateLimits:list[_RateLimit]
    assets:list[_Asset]
    symbols:list[_Symbols]

class ExchangeInfoKwargs(RequestConfig):...

class AutoCancelOrderReturn(MyBaseModel):
    symbol:str
    countdownTime:Decimal

class AutoCancelOrderKwargs(SecureRequestConfig):
    symbol:str
    countdownTime:int

class CancelAllOrderReturn(MyBaseModel):
    code:int
    msg:str
    
class CancelAllOrderKwargs(SecureRequestConfig):
    symbol:str

class ModifyOrderReturn(MyBaseModel):
    order_id:int=Field(alias="orderId")
    symbol:str
    status:OrderStatus 
    client_order_id:str=Field(alias="clientOrderId")
    price:Decimal
    avg_price:Decimal=Field(alias="avgPrice")
    orig_qty:Decimal=Field(alias="origQty")
    executed_qty:Decimal=Field(alias="executedQty")
    cum_qty:Decimal=Field(alias="cumQty")
    cum_quote:Decimal=Field(None, alias="cumQuote")
    time_in_force:TimeInForce=Field(alias="timeInForce")
    type:OrderType
    reduce_only:bool=Field(alias="reduceOnly")
    close_position:bool=Field(alias="closePosition")
    side:OrderSide
    position_side:PositionSide=Field(alias="positionSide")
    stop_price:Decimal=Field(alias="stopPrice")
    working_type:str=Field(alias="workingType")
    price_protect:bool=Field(alias="priceProtect")
    orig_type:OrderType=Field(alias="origType")
    price_match:PriceMatch=Field(alias="priceMatch")
    self_trade_prevention_mode:str=Field(alias="selfTradePreventionMode")
    good_till_date:int=Field(alias="goodTillDate")
    update_time:int=Field(alias="updateTime")

class ModifyOrderKwargs(SecureRequestConfig):
    orderId:Optional[int]=None
    origClientOrderId:Optional[str]=None
    symbol:str
    side:OrderSide
    quantity:Decimal
    price:Optional[Decimal]=None
    priceMatch:Optional[PriceMatch]=None

class ContKlineReturn(RootModel):
    # The 'root' is a list of lists (the raw Binance response)
    root:List[List[Any]]

    @field_validator("root", mode="after")
    @classmethod
    def to_dataframe(cls, v: List[List[Any]]) -> pd.DataFrame:
        # Define the standard Binance Kline columns
        columns = [
            "open_time", "open_price", "high_price", "low_price", "close_price", 
            "volume", "close_time", "quote_asset_volume", "trade_num",
            "taker_buy_volume", "taker_buy_quote_asset_volume", "ignore"
        ]
        
        df = pd.DataFrame(v, columns=columns)
        
        # Convert numeric columns from strings to floats
        decimal_cols = [
            "open_price", "high_price", "low_price", "close_price", 
            "volume", "quote_asset_volume", "taker_buy_volume", "taker_buy_quote_asset_volume"]
        for col in decimal_cols:
            df[col] = df[col].apply(Decimal)
            
        return df

    # This allows you to call .dataframe on the object easily
    @property
    def df(self) -> pd.DataFrame:
        return self.root

class ContKlineKwargs(RequestConfig):
    pair:str
    interval:CandleInterval
    contractType:ContractType
    startTime:Optional[int]=None
    endTime: Optional[int]=None
    limit: Optional[int]=None

class SymbolPriceTickerReturn(MyBaseModel):
    symbol:str
    price:Decimal
    trans_time:int=Field(alias="time")

class SymbolPriceTickerKwargs(RequestConfig):
    symbol:str

class OrderBookTickerReturn(MyBaseModel):
    last_update_id:int=Field(None, alias="lastUpdateId") # not on the rest doc example output but actually in it
    symbol:str
    bid_price:Decimal=Field(alias="bidPrice")
    bid_qty:Decimal=Field(alias="bidQty")
    ask_price:Decimal=Field(alias="askPrice")
    ask_qty:Decimal=Field(alias="askQty")
    trans_time:int=Field(alias="time")

class OrderBookTickerKwargs(RequestConfig):
    symbol:str

class NewOrderReturn(MyBaseModel):
    client_order_id:str=Field(alias="clientOrderId")
    cum_qty:Decimal=Field(alias="cumQty")
    cum_quote:Decimal=Field(alias="cumQuote")
    executed_qty:Decimal=Field(alias="executedQty")
    order_id:int=Field(alias="orderId")
    avg_price:Decimal=Field(alias="avgPrice")
    orig_qty:Decimal=Field(alias="origQty")
    price:Decimal
    reduce_only:bool=Field(alias="reduceOnly")
    side:OrderSide
    position_side:PositionSide=Field(alias="positionSide")
    status:OrderStatus
    stop_price:Decimal=Field(alias="stopPrice")
    close_position:bool=Field(alias="closePosition") # if close all
    symbol:str
    time_in_force:TimeInForce=Field(alias="timeInForce")
    type:OrderType
    orig_type:OrderType=Field(alias="origType")
    update_time:int=Field(alias="updateTime")
    working_type:str=Field(alias="workingType")
    price_protect:bool=Field(alias="priceProtect")
    price_match:str=Field(alias="priceMatch")
    self_trade_prevention_mode:str=Field(alias="selfTradePreventionMode")
    good_till_date:int=Field(alias="goodTillDate")

class NewOrderKwargs(SecureRequestConfig):
    symbol:str
    side:OrderSide
    positionSide:Optional[PositionSide] = None
    type:OrderType
    timeInForce:Optional[TimeInForce] = None
    quantity:Optional[Decimal] = None
    reduceOnly:Optional[str] = None
    price:Optional[Decimal] = None
    newClientOrderId:Optional[str] = None
    newOrderRespType:Optional[str] = None
    priceMatch:Optional[PriceMatch] = None
    selfTradePreventionMode:Optional[str] = None
    goodTillDate:Optional[int] = None

class CancelOrderReturn(MyBaseModel):
    client_order_id:str=Field(alias="clientOrderId")
    cum_qty:Decimal=Field(alias="cumQty")
    cum_quote:Decimal=Field(alias="cumQuote")
    executed_qty:Decimal=Field(alias="executedQty")
    order_id:int=Field(alias="orderId")
    order_qty:Decimal=Field(alias="origQty")
    orig_type:OrderType=Field(alias="origType")
    price:Decimal
    avg_price:Decimal=Field(alias="avgPrice")
    reduce_only:bool=Field(alias="reduceOnly")
    side:OrderSide
    position_side:PositionSide=Field(alias="positionSide")
    status:OrderStatus
    stop_price:Decimal=Field(alias="stopPrice")
    close_position:bool=Field(alias="closePosition")
    symbol:str
    time_in_force:TimeInForce=Field(alias="timeInForce")
    type:OrderType
    update_time:int=Field(alias="updateTime")
    working_type:str=Field(alias="workingType")
    price_protect:bool=Field(alias="priceProtect")
    price_match:str=Field(alias="priceMatch")
    self_trade_prevention_mode:str=Field(alias="selfTradePreventionMode")
    good_till_date:int=Field(alias="goodTillDate")

class CancelOrderKwargs(SecureRequestConfig):
    symbol:str
    orderId:Optional[int]=None
    origClientOrderId:Optional[str]=None

class QueryOrderReturn(MyBaseModel):
    avg_price:Decimal=Field(alias="avgPrice")
    client_order_id:str=Field(alias="clientOrderId")
    cum_quote:Decimal=Field(alias="cumQuote")
    executed_qty:Decimal=Field(alias="executedQty")
    order_id:int=Field(alias="orderId")
    orig_qty:Decimal=Field(alias="origQty")
    orig_type:OrderType=Field(alias="origType")
    price:Decimal
    reduce_only:bool=Field(alias="reduceOnly")
    side:OrderSide
    position_side:PositionSide=Field(alias="positionSide")
    status:OrderStatus
    stop_price:Decimal=Field(alias="stopPrice")
    close_position:bool=Field(alias="closePosition")
    symbol:str
    time:int # order time
    time_in_force:TimeInForce=Field(alias="timeInForce")
    type:OrderType
    update_time:int=Field(alias="updateTime")
    working_type:str=Field(alias="workingType")
    price_protect:bool=Field(alias="priceProtect")
    #extra that's not in the example
    price_match:PriceMatch=Field(alias="priceMatch")
    self_trade_prevention_mode:str=Field(alias="selfTradePreventionMode")
    good_till_date:int=Field(alias="goodTillDate")

class QueryOrderKwargs(SecureRequestConfig):
    symbol:str
    orderId:Optional[int]
    origClientOrderId:Optional[str]

class ChangeMarginTypeReturn(MyBaseModel):
    code:int
    msg:str

class ChangeMarginTypeKwargs(SecureRequestConfig):
    symbol:str
    margintype:MarginType

class ChangePositionModeReturn(MyBaseModel):
    code:int
    msg:str

class ChangePositionModeKwargs(SecureRequestConfig):
    dualSidePosition:bool

class ChangeLeverageReturn(MyBaseModel):
    leverage:int
    max_notional_value:Decimal=Field(alias="maxNotionalValue")
    symbol:str

class ChangeLeverageKwargs(SecureRequestConfig):
    symbol:str
    leverage:int

class ChangeMultiAssetsModeReturn(MyBaseModel):
    code:int
    msg:str

class ChangeMultiAssetsModeKwargs(SecureRequestConfig):
    multiAssetsMargin:bool

class _SymbolItem(MyBaseModel):
    symbol:str
    margin_type:MarginType=Field(alias="marginType")
    is_auto_add_margin:bool=Field(alias="isAutoAddMargin")
    leverage:int
    max_notional_value:Decimal=Field(alias="maxNotionalValue")

class SymbolConfigReturn(RootModel):
    root: List[_SymbolItem]

    def get_symbol(self, symbol:str) -> _SymbolItem|None:
        """Finds a balance item by its asset name (e.g., 'USDT')."""
        return next((item for item in self.root if item.asset == symbol), None)

    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, item)->_SymbolItem:
        return self.root[item]

class SymbolConfigKwargs(SecureRequestConfig):
    symbol:bool

class _PositionItem(MyBaseModel):
    symbol:str
    position_side:PositionSide=Field(alias="positionSide")
    position_amt:Decimal=Field(alias="positionAmt")
    entry_price:Decimal=Field(alias="entryPrice")
    break_even_price:Decimal=Field(alias="breakEvenPrice")
    mark_price:Decimal=Field(alias="markPrice")
    un_realized_profit:Decimal=Field(alias="unRealizedProfit")
    liquidation_price:Decimal=Field(alias="liquidationPrice")
    isolated_margin:Decimal=Field(alias="isolatedMargin")
    notional:Decimal
    margin_asset:str=Field(alias="marginAsset")
    isolated_wallet:Decimal=Field(alias="isolatedWallet")
    initial_margin:Decimal=Field(alias="initialMargin")
    maint_margin:Decimal=Field(alias="maintMargin")
    position_initial_margin:Decimal=Field(alias="positionInitialMargin")
    open_order_initial_argin:Decimal=Field(alias="openOrderInitialMargin")
    adl:int
    bid_notional:Decimal=Field(alias="bidNotional")
    ask_notional:Decimal=Field(alias="askNotional")
    update_time:int=Field(alias="updateTime")

class PositionInfoReturn(RootModel):
    root:List[_PositionItem]

    def get_position(self, symbol:str, position_side:PositionSide):
        return next((item for item in self.root if item.symbol==symbol and item.position_side==position_side), None)

    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, item)->_PositionItem:
        return self.root[item]
    
class PositionInfoKwargs(SecureRequestConfig):
    Symbol:str

class _BalanceItem(MyBaseModel):
    account_alias:str=Field(alias="accountAlias")
    asset:str
    balance:Decimal
    cross_wallet_balance:Decimal=Field(alias="crossWalletBalance")
    cross_unrealized_profit:Decimal=Field(alias="crossUnPnl")
    available_balance:Decimal=Field(alias="availableBalance")
    max_withdraw_amount:Decimal=Field(alias="maxWithdrawAmount")
    margin_available:bool=Field(alias="marginAvailable")
    update_time:int=Field(alias="updateTime")

class AccountBalanceReturn(RootModel):
    '''rest/ws'''
    root:List[_BalanceItem]

    def get_asset(self, asset_name: str)->_BalanceItem|None:
        """Finds a balance item by its asset name (e.g., 'USDT')."""
        return next((item for item in self.root if item.asset == asset_name.upper()), None)

    def __iter__(self):
        return iter(self.root)
    
    def __getitem__(self, item)->_BalanceItem:
        return self.root[item]
    
class AccountBalanceKwargs(SecureRequestConfig):...

class AccountConfigReturn(MyBaseModel):
    fee_tier:int=Field(alias="feeTier")
    can_trade:bool=Field(alias="canTrade")
    can_deposit:bool=Field(alias="canDeposit")
    can_withdraw:bool=Field(alias="canWithdraw")
    dual_side_position:bool=Field(alias="dualSidePosition")
    update_time:int=Field(alias="updateTime")
    multi_assets_margin:bool=Field(alias="multiAssetsMargin")
    trade_group_id:int=Field(alias="tradeGroupId")

class AccountConfigKwargs(SecureRequestConfig):...

class EndPoint(MyBaseModel, Generic[P, R]):
    endpoint:str
    method:RequestMethod
    param_type:Type[P]
    return_type:Type[R]

class RestEndpointCollection(Enum):
    # unsigned
    SERVER_TIME = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v1/time",
        param_type=ServerTimeKwargs,
        return_type=ServerTimeReturn,
    )

    # unsigned
    EXCHANGE_INFO = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v1/exchangeInfo",
        param_type=ExchangeInfoKwargs,
        return_type=ExchangeInfoReturn,
    )

    # unsigned
    CONT_KLINE = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v1/continuousKlines",
        param_type=ContKlineKwargs,
        return_type=ContKlineReturn,
    )

    # unsigned
    ORDER_BOOK_TICKER = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v1/ticker/bookTicker",
        param_type=OrderBookTickerKwargs,
        return_type=OrderBookTickerReturn,
    )

    # unsigned
    SYMBOL_PRICE_TICKER = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v2/ticker/price",
        param_type=SymbolPriceTickerKwargs,
        return_type=SymbolPriceTickerReturn,
    )

    # signed
    NEW_ORDER = EndPoint(
        method=RequestMethod.POST,
        endpoint="/fapi/v1/order",
        param_type=NewOrderKwargs,
        return_type=NewOrderReturn,
    )

    # signed
    CANCEL_ORDER = EndPoint(
        method=RequestMethod.DELETE,
        endpoint="/fapi/v1/order",
        param_type=CancelOrderKwargs,
        return_type=CancelOrderReturn,
    )

    # signed
    QUERY_ORDER = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v1/order",
        param_type=QueryOrderKwargs,
        return_type=QueryOrderReturn,
    )

    # signed
    MODIFY_ORDER = EndPoint(
        method=RequestMethod.PUT,
        endpoint="/fapi/v1/order",
        param_type=ModifyOrderKwargs,
        return_type=ModifyOrderReturn,
    )

    # signed
    CHANGE_MARGIN_TYPE = EndPoint(
        method=RequestMethod.POST,
        endpoint="/fapi/v1/marginType",
        param_type=ChangeMarginTypeKwargs,
        return_type=ChangeMarginTypeReturn,
    )

    # signed
    # need no exist order to change
    CHANGE_POSITION_MODE = EndPoint( 
        method=RequestMethod.POST,
        endpoint="/fapi/v1/positionSide/dual",
        param_type=ChangePositionModeKwargs,
        return_type=ChangePositionModeReturn,
    )

    # signed
    CHANGE_LEVERAGE = EndPoint(
        method=RequestMethod.POST,
        endpoint="/fapi/v1/leverage",
        param_type=ChangeLeverageKwargs,
        return_type=ChangeLeverageReturn,
    )

    # signed
    CHANGE_MULTI_ASSETS_MODE = EndPoint(
        method=RequestMethod.POST,
        endpoint="/fapi/v1/multiAssetsMargin",
        param_type=ChangeMultiAssetsModeKwargs,
        return_type=ChangeMultiAssetsModeReturn,
    )

    # signed
    ACCOUNT_BALANCE = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v3/balance",
        param_type=AccountBalanceKwargs,
        return_type=AccountBalanceReturn,
    )

    # signed
    ACCOUNT_CONFIG = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v1/accountConfig",
        param_type=AccountConfigKwargs,
        return_type=AccountConfigReturn,
    )

    # signed
    SYMBOL_CONFIG = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v1/symbolConfig",
        param_type=SymbolConfigKwargs,
        return_type=SymbolConfigReturn,
    )

    # signed
    CANCEL_ALL_ORDER = EndPoint(
        method=RequestMethod.DELETE,
        endpoint="/fapi/v1/allOpenOrders",
        param_type=CancelAllOrderKwargs,
        return_type=CancelAllOrderReturn,
    )

    # signed
    AUTO_CANCEL_ORDER = EndPoint(
        method=RequestMethod.POST,
        endpoint="/fapi/v1/countdownCancelAll",
        param_type=AutoCancelOrderKwargs,
        return_type=AutoCancelOrderReturn,
    )

    # signed
    POSITION_INFO = EndPoint(
        method=RequestMethod.GET,
        endpoint="/fapi/v3/positionRisk",
        param_type=PositionInfoKwargs,
        return_type=PositionInfoReturn,
    )