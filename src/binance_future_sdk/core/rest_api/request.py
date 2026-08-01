import requests
from typing import Optional
import logging

from .schema import (
    R, P,
    EndPoint
)
from .const import BaseUrl, BinanceError

logger = logging.getLogger(__name__)

def handle_api_error(response: requests.Response):
    try:
        json_res:dict = response.json()
        code = json_res.get("code")
        msg = json_res.get("msg")
        raise Exception(f"{response.status_code} API Error {code} {BinanceError.get_by_code(code)}: {msg}")
    except ValueError:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def request(endpoint: EndPoint[P, R], kwargs: Optional[P] = None, test: bool = False) -> R:
    base_url = BaseUrl.TEST_URL if test else BaseUrl.URL
    full_url = f"{base_url}{endpoint.endpoint}"
    headers = kwargs.header() if kwargs else {}
    query_str = kwargs.query() if kwargs else ""

    req_kwargs = {
        "method":f"{endpoint.method}",
        "url":full_url,
        "headers":headers,
        "params":query_str # data could be passed as params or data binance accept both
    }

    logging.debug(f"req kwargs: {req_kwargs}")
    response = requests.request(**req_kwargs)
    logging.debug(f"req result: {response.status_code} {response.text}")
    if response.status_code >= 400:
        handle_api_error(response)
        
    return endpoint.return_type.model_validate(response.json())
