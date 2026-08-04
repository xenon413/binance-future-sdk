import logging

logger = logging.getLogger(__name__)

class BinanceRestAPIError(Exception):
    """Custom exception for Binance REST API errors."""
    def __init__(self, message: str):
        super().__init__(message)
        logger.error(f"BinanceRestAPIError: {message}")
