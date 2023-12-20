#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an
instance of the Redis client as a private variable named
_redis (using redis.Redis()) and flush the instance using flushdb.
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count how many times methods of the Cache class are called.
    """
    @wraps(method)
    def counter(self, *args, **kwargs) -> Any:
        """
        ...
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return counter


def call_history(method: Callable) -> Callable:
    """
    This is a decorator to store the history of inputs and
    outputs for a particular function
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def counter(self, *args, **kwargs):
        """ Wrapp """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return counter


def replay(fn: Callable) -> None:
    """
    ...
    """
    pass


class Cache():
    """
    Cache class
    """
    _redis = None

    def __init__(self) -> None:
        """
        init
        store an instance of the Redis client as a private
        variable named _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generate a random key using uuid then
        returns a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Callable = None) -> Union[
                str, int, float, bytes]:
        """
        used to convert the data back to the desired format.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> str:
        """
        returns a str
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        returns an int
        """
        return self.get(key, lambda x: int(x))


if __name__ == "__main__":
    cache = Cache()
    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
        print(f"{value}: {cache.get(key, fn=fn)}")
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
