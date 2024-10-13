import requests
from functools import wraps
from typing import Dict, Any, Optional

from enum import Enum

class MockResponse:
    def __init__(self, status_code: int, content: str, json_data: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.text = content
        self._json = json_data

    def json(self):
        if self._json is None:
            raise ValueError("No JSON data available")
        return self._json

def mock_api(status_code: int, content: str, json_data: Optional[Dict[str, Any]] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mock_response = MockResponse(status_code, content, json_data)
            kwargs['status_code'] = mock_response.status_code
            kwargs['response_content'] = mock_response.text
            try:
                kwargs['response_json'] = mock_response.json()
            except ValueError:
                pass
            return func(*args, **kwargs)
        return wrapper
    return decorator

def api(method: str, url: str, headers: Optional[Dict[str, str]] = None, 
        cookies: Optional[Dict[str, str]] = None, data: Optional[Dict[str, Any]] = None, 
        json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, str]] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                cookies=cookies,
                data=data,
                json=json,
                params=params
            )
            kwargs['status_code'] = response.status_code
            kwargs['response_content'] = response.text
            try:
                kwargs['response_json'] = response.json()
            except ValueError:
                kwargs['response_json'] = None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


