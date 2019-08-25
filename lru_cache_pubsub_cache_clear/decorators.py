from functools import update_wrapper

from redis.client import PubSubWorkerThread

functions: list = []
pubsub = None


def lru_cache_pubsub_cache_clear(get_redis_connection, channel_name):

    def decorating_function(f):
        global pubsub

        if hasattr(f, 'cache_clear'):

            def f_cache_clear(message) -> None:
                for f in functions:
                    if message['type'] == 'message' and message['data'].decode() == f.__name__:
                        f.cache_clear()

            if pubsub is None:
                try:
                    pubsub = get_redis_connection().pubsub()
                    pubsub.subscribe(**{channel_name: f_cache_clear})
                    PubSubWorkerThread(pubsub, sleep_time=None, daemon=True).start()
                except NotImplementedError:
                    pass

        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        def cache_clear():
            f.cache_clear()
            try:
                redis = get_redis_connection()
                redis.publish(channel_name, f.__name__)
            except NotImplementedError:
                pass

        functions.append(f)

        wrapper.__wrapped__ = f
        if hasattr(f, 'cache_info'):
            wrapper.cache_info = f.cache_info
        if hasattr(f, 'cache_clear'):
            wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, f)

    return decorating_function
