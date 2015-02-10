#coding: utf8
from cachecore import SimpleCache, MemcachedCache, RedisCache, FileSystemCache
try:
    import cPickle as pickle
except ImportError:
    import pickle

# decorator for cache 
def cache_func(cache_instance):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = '%s:%s|' % (func.__module__, func.__name__) + repr((args, kwargs))
            result = self.get(key)
            if result:
                return result
            else:
                value = func(*args, **kwargs)
                self.set(key, value)
                return value