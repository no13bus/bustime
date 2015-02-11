#coding: utf8
# decorator for cache 
def cache_func(cache_instance, timeout=None):
    def dec(func):
        def wrapper(*args, **kwargs):
            key = '%s:%s|' % (func.__module__, func.__name__) + repr((args, kwargs))
            result = cache_instance.get(key)
            if result:
                return result
            else:
                value = func(*args, **kwargs)
                if value:
                    cache_instance.set(key, value)
                    return value
                else:
                    return None
        return wrapper
    return  dec