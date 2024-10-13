import threading
from typing import Dict, Any
import functools

class ThreadLocalCache:
    def __init__(self):
        self._local = threading.local()

    def set(self, key: str, value: Any) -> None:
        if not hasattr(self._local, 'cache'):
            self._local.cache = {}
        self._local.cache[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        if not hasattr(self._local, 'cache'):
            return default
        return self._local.cache.get(key, default)

    def clear(self) -> None:
        if hasattr(self._local, 'cache'):
            self._local.cache.clear()

http_response_cache = ThreadLocalCache()

def cache_http_response(key: str, content: Any) -> None:
    """
    缓存HTTP响应内容
    :param key: 缓存的键
    :param content: 要缓存的响应内容
    """
    http_response_cache.set(key, content)

def get_cached_http_response(key: str, default: Any = None) -> Any:
    """
    获取缓存的HTTP响应内容
    :param key: 缓存的键
    :param default: 如果键不存在时返回的默认值
    :return: 缓存的响应内容，如果不存在则返回默认值
    """
    return http_response_cache.get(key, default)

def clear_http_response_cache() -> None:
    """
    清除当前线程的HTTP响应缓存
    """
    http_response_cache.clear()


import functools

def cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            for key, value in result.items():
                cache_http_response(key, value)
        return result
    return wrapper

def cache_ware(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        param_names = func.__code__.co_varnames[:func.__code__.co_argcount]
        for param in param_names:
            if param not in kwargs:
                cached_value = get_cached_http_response(param)
                if cached_value is not None:
                    kwargs[param] = cached_value
        
        result = func(*args, **kwargs)
        return result
    return wrapper
