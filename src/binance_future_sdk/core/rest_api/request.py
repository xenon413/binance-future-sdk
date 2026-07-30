import requests
from typing import Optional
from .schema import (
    R, P,
    EndPoint
)
from .const import BaseUrl, RequestMethod

def handle_api_error(response: requests.Response):
    try:
        json_res = response.json()
        code = json_res.get("code")
        msg = json_res.get("msg")
        raise Exception(f"API Error {code}: {msg}")
    except ValueError:
        raise Exception(f"API Error {response.status_code}: {response.text}")

def request(endpoint: EndPoint[P, R], kwargs: Optional[P] = None, test: bool = False) -> R:
    base_url = BaseUrl.TEST_URL if test else BaseUrl.URL
    
    path = endpoint.endpoint
    full_url = f"{base_url}{path}" if path.startswith('/') else f"{base_url}/{path}"
        
    headers = kwargs.header() if kwargs else {}
    query_str = kwargs.query() if kwargs else ""
    
    req_kwargs = {
        "method": endpoint.method,
        "url": full_url,
        "headers": headers,
        "params":query_str # data could be passed as params or data binance accept both
    }

    response = requests.request(**req_kwargs)
    
    if response.status_code >= 400:
        handle_api_error(response)
        
    return endpoint.return_type.model_validate(response.json())
