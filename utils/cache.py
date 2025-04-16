from functools import lru_cache

@lru_cache(maxsize=128)
def cached_keywords(topic: str) -> list:
    from utils.api_clients import fetch_datamuse
    import asyncio
    return asyncio.run(fetch_datamuse(topic))

@lru_cache(maxsize=64)
def cached_quotes(topic: str) -> list:
    from utils.api_clients import fetch_quotable
    import asyncio
    return asyncio.run(fetch_quotable(topic))