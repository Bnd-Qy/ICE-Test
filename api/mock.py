import functools
from unittest.mock import patch
from requests import Response
from typing import Dict, Any, Optional

def mock_api(status_code: int, content: str, json_data: Optional[Dict[str, Any]] = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mock_response = Response()
            mock_response.status_code = status_code
            mock_response._content = content.encode('utf-8')
            
            if json_data is not None:
                mock_response.json = lambda: json_data

            with patch('requests.request', return_value=mock_response):
                return func(*args, **kwargs)
        return wrapper
    return decorator

def api(method: str, url: str, headers: Optional[Dict[str, str]] = None, 
        cookies: Optional[Dict[str, str]] = None, data: Optional[Dict[str, Any]] = None, 
        json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, str]] = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            from api.local_variable import get_cached_http_response

            # 处理URL中的变量
            processed_url = url
            for key, value in kwargs.items():
                if f'${key}' in processed_url:
                    processed_url = processed_url.replace(f'${key}', str(value))

            # 处理headers中的变量
            processed_headers = headers.copy() if headers else {}
            for key, value in processed_headers.items():
                if value.startswith('$'):
                    var_name = value[1:]
                    cached_value = get_cached_http_response(var_name)
                    if cached_value is not None:
                        processed_headers[key] = cached_value

            # 处理cookies中的变量
            processed_cookies = cookies.copy() if cookies else {}
            for key, value in processed_cookies.items():
                if isinstance(value, str) and value.startswith('$'):
                    var_name = value[1:]
                    cached_value = get_cached_http_response(var_name)
                    if cached_value is not None:
                        processed_cookies[key] = cached_value

            # 处理data中的变量
            processed_data = data.copy() if data else {}
            for key, value in processed_data.items():
                if isinstance(value, str) and value.startswith('$'):
                    var_name = value[1:]
                    cached_value = get_cached_http_response(var_name)
                    if cached_value is not None:
                        processed_data[key] = cached_value

            # 处理json中的变量
            processed_json = json.copy() if json else {}
            for key, value in processed_json.items():
                if isinstance(value, str) and value.startswith('$'):
                    var_name = value[1:]
                    cached_value = get_cached_http_response(var_name)
                    if cached_value is not None:
                        processed_json[key] = cached_value

            # 处理params中的变量
            processed_params = params.copy() if params else {}
            for key, value in processed_params.items():
                if isinstance(value, str) and value.startswith('$'):
                    var_name = value[1:]
                    cached_value = get_cached_http_response(var_name)
                    if cached_value is not None:
                        processed_params[key] = cached_value

            if hasattr(func, '_mock_response'):
                mock_response = func._mock_response
                kwargs['status_code'] = mock_response.status_code
                kwargs['response_content'] = mock_response._content.decode('utf-8')
                try:
                    kwargs['response_json'] = mock_response.json()
                except ValueError:
                    pass
            else:
                from .http import api as original_api
                return original_api(method, processed_url, processed_headers, cookies, data, json, params)(func)(*args, **kwargs)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


