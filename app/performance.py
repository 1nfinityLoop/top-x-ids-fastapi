import cProfile
import pstats
import io
import tracemalloc
from functools import wraps

def profile_memory(func):
    """Decorator to profile memory usage"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = await func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Memory Usage: Current={current / 10**6} MB, Peak={peak / 10**6} MB")
        return result
    return wrapper

def profile_execution_time(func):
    """Decorator to profile execution time"""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return result
    return wrapper
