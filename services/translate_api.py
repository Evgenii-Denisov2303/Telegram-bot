import logging


logger = logging.getLogger(__name__)


async def translate_text(session, settings, cache, text, target_language="ru"):
    if not text:
        return None

    cache_key = f"translate:{target_language}:{text}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    params = {
        "client": "gtx",
        "sl": "en",
        "tl": target_language,
        "dt": "t",
        "q": text,
    }

    try:
        async with session.get(settings.translate_api_url, params=params) as response:
            response.raise_for_status()
            result = await response.json(content_type=None)
            translated = result[0][0][0] if result else None
            if translated:
                cache.set(cache_key, translated, ttl=600)
            return translated
    except Exception as exc:
        logger.warning("Translate API error: %s", exc)
        return None
