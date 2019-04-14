# lru_cache_pubsub_cache_clear
`lru_cache_pubsub_cache_clear` is a decorator to broadcast `cache_clear()` calls to `lru_cache` across
multiple instances of an application.

```
@lru_cache_pubsub_cache_clear(redis_connection, channel_name, sleep_time)
@lru_cache
def cache_data(key, value)
    ...
``` 