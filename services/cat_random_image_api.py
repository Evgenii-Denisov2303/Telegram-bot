import logging


logger = logging.getLogger(__name__)


async def fetch_random_cat_image(session, settings):
    try:
        async with session.get(settings.cat_api_url) as response:
            response.raise_for_status()
            data = await response.json()
            if not data or not isinstance(data, list):
                return None
            return data[0].get("url")
    except Exception as exc:
        logger.warning("Cat image API error: %s", exc)
        return None
