#!/usr/bin/env python3
"""
web.py
"""
import redis
import requests
from typing import Callable
from functools import wraps

redis = redis.Redis()


def main_wrapper(fn: Callable) -> Callable:
    """
    Decorator
    """
    @wraps(fn)
    def wrapper(url):
        """
        Wrapper
        """
        url = f"cont:{url}"
        redis.incr(url)
        response = redis.get(f"ccched:{url}")
        if response:
            return response.decode("utf-8")
        ret = fn(url)
        redis.setex(f"cached:{url}", 10, ret)
        return ret
    return wrapper


def get_page(url: str) -> str:
    """
    uses the requests module to obtain the HTML content of a
    particular URL and returns it.
    """
    return requests.get(url).text

# if __name__ == "__main__":
#     url = "http://slowwly.robertomurray.co.uk"
#     print(redis.get(f"count:{url}"))
#     print(get_page(url))
#     get_page(url)
#     print(get_page)
#     print(redis.get(f"count:{url}"))
