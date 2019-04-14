# lru_cache_pubsub_cache_clear
`lru_cache_pubsub_cache_clear` is a decorator to broadcast `cache_clear()` calls to `lru_cache` across
multiple instances of an application. This allows for local cache access speed. Example:

```
from lru_cache_pubsub_cache_clear import lru_cache_pubsub_cache_clear
from django_redis import get_redis_connection


@lru_cache_pubsub_cache_clear(redis_connection=get_redis_connection(),
                              channel_name='CHANNEL_CACHE_CLEAR',
                              sleep_time=3)
@lru_cache
def cache_data(key, value)
    ...
```
Here `sleep_time` is interval (in seconds) between pubsub message checks.


Then every time one of app instances calls `cache_data.cache_clear()` it will be executed on all connected instances.