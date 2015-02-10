#coding: utf8
from cachecore import SimpleCache, MemcachedCache, RedisCache, FileSystemCache

# decorator for cache 
def cache_func(cache_instance, timeout=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = '%s:%s|' % (func.__module__, func.__name__) + repr((args, kwargs))
            result = cache_instance.get(key)
            if result:
                return result
            else:
                value = func(*args, **kwargs)
                if value:
                    cache_instance.set(key, value, timeout)
                    return value
                else:
                    return
        return wrapper
    return decorator

