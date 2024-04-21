from collections import OrderedDict
from typing import TypeVar, Callable

P = TypeVar("P")
R = TypeVar("R")


def cached(
        fn: Callable[[P], R],
        cache_size: int = 10
) -> Callable[[P], R]:
    cache: OrderedDict[P, R] = OrderedDict(dict())
    return lambda p: call_with_cache(fn, p, cache, cache_size)


def call_with_cache(
        fn: Callable[[P], R],
        p: P,
        cache: OrderedDict[P, R],
        cache_size: int
) -> R:
    if p in cache:
        cache.move_to_end(p)
        return cache[p]
    result = fn(p)
    cache[p] = result
    if len(cache) >= cache_size:
        cache.popitem(last=False)
    return result
