import functools
import time
from typing import Callable, Any

benchmark = {}

def timer(key: str | None = 'time') -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if key is not None:
                start_time = time.perf_counter()
                value = func(*args, **kwargs)
                benchmark[key] = time.perf_counter() - start_time
            else:
                value = func(*args, **kwargs)
            return value
        return wrapper
    return decorator
