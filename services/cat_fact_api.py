import logging


logger = logging.getLogger(__name__)


async def fetch_cat_fact(session, settings, cache):
    cache_key = "cat_fact"
    cached = cache.get(cache_key)
    if cached:
        return cached

    try:
        async with session.get(settings.cat_facts_api_url) as response:
            response.raise_for_status()
            data = await response.json()
            fact = data.get("fact")
            if fact:
                cache.set(cache_key, fact, ttl=5)
            return fact
    except Exception as exc:
        logger.warning("Cat fact API error: %s", exc)
        return None
