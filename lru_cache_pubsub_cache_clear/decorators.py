from functools import update_wrapper

from redis.client import PubSubWorkerThread


def lru_cache_pubsub_cache_clear(redis_connection, channel_name, sleep_time):

    def decorating_function(f):
        if hasattr(f, 'cache_clear'):

            def f_cache_clear(message) -> None:
                if message['type'] == 'message' and message['data'].decode() == f.__name__:
                    f.cache_clear()

            try:
                pubsub = redis_connection.pubsub()
                pubsub.subscribe(**{channel_name: f_cache_clear})
                PubSubWorkerThread(pubsub, sleep_time=sleep_time, daemon=True).start()
            except NotImplementedError:
                pass

        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        def cache_clear():
            f.cache_clear()
            try:
                redis = redis_connection
                redis.publish(channel_name, f.__name__)
            except NotImplementedError:
                pass

        wrapper.__wrapped__ = f
        if hasattr(f, 'cache_info'):
            wrapper.cache_info = f.cache_info
        if hasattr(f, 'cache_clear'):
            wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, f)

    return decorating_function
