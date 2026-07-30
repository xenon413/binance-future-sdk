# binance-future-sdk

Python SDK for the Binance Futures REST API with typed helpers for market data,
order management, and account operations.

## Features

- Query market and exchange information such as server time, exchange rules,
  continuous klines, order book tickers, and symbol price tickers.
- Submit and manage futures orders with helpers for creating, canceling,
  querying, and modifying orders.
- Access account and position settings including balances, leverage, margin
  type, position mode, and multi-assets mode.
- Support for Binance Futures testnet via the built-in `test=True` flag.

## Installation

Install the package from GitHub:

```bash
pip install git+https://github.com/xenon413/binance-future-sdk.git@main
```

## Quick Start

```python
from binance_future_sdk.core.rest_api import get_server_time, get_symbol_price_ticker

server_time = get_server_time(test=True)
print(server_time.server_time)

price = get_symbol_price_ticker("BTCUSDT", test=True)
print(price.symbol, price.price)
```

## Example: Place a Test Order

```python
import os
from decimal import Decimal

from binance_future_sdk.core.rest_api import new_order
from binance_future_sdk.core.rest_api.const import OrderSide, OrderType, TimeInForce

new_order(
    key=os.environ["BINANCE_API_KEY"],
    secret=os.environ["BINANCE_API_SECRET"],
    symbol="BTCUSDT",
    side=OrderSide.BUY,
    type=OrderType.LIMIT,
    quantity=Decimal("0.001"),
    price=Decimal("10000"),
    timeInForce=TimeInForce.GTC,
    test=True,
)
```

Set the `BINANCE_API_KEY` and `BINANCE_API_SECRET` environment variables before
running authenticated requests.

## Development & Testing

Clone the repository and install it in editable mode with the test dependencies:

```bash
git clone https://github.com/xenon413/binance-future-sdk.git
cd binance-future-sdk
pip install -e .[test]
```

Run the unit-style tests (excluding live integration checks):

```bash
pytest -m "not integration"
```

Run the full test suite, including integration tests that use the live API or
network-dependent behavior:

```bash
pytest
```

## Public API Overview

The main helpers are exposed from `binance_future_sdk.core.rest_api`:

- `get_server_time(test: bool = False)`
- `get_exchange_info(test: bool = False)`
- `get_cont_kline(...)`
- `get_order_book_ticker(symbol: str, test: bool = False)`
- `get_symbol_price_ticker(symbol: str, test: bool = False)`
- `new_order(...)`
- `cancel_order(...)`
- `query_order(...)`
- `modify_order(...)`
- `change_margin_type(...)`
- `change_position_mode(...)`
- `change_leverage(...)`
- `change_multi_assets_mode(...)`
- `get_account_balance(...)`
- `get_account_config(...)`
- `get_symbol_config(...)`
- `cancel_all_order(...)`
- `auto_cancel_order(...)`
- `get_position_info(...)`

## License

See the repository `LICENSE` file for license details.
