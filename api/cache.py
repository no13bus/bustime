#coding: utf8
<<<<<<< HEAD
from cachecore import SimpleCache, MemcachedCache, RedisCache, FileSystemCache

# decorator for cache 
def cache_func(cache_instance, timeout=None):
    def decorator(func):
=======


# decorator for cache 
def cache_func(cache_instance, timeout=None):
    def dec(func):
>>>>>>> 42531fcac1a5f79b57e0577a253db88a0a58f6c9
        def wrapper(*args, **kwargs):
            key = '%s:%s|' % (func.__module__, func.__name__) + repr((args, kwargs))
            result = cache_instance.get(key)
            if result:
                return result
            else:
                value = func(*args, **kwargs)
<<<<<<< HEAD
                if value:
                    cache_instance.set(key, value, timeout)
                    return value
                else:
                    return
        return wrapper
    return decorator

=======
                cache_instance.set(key, value)
                return value
        return wrapper
    return  dec
>>>>>>> 42531fcac1a5f79b57e0577a253db88a0a58f6c9
