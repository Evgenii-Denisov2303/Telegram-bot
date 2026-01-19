import asyncio
import logging

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data.config import load_settings
from database.db_setup import init_db
from handlers import get_routers
from utils.set_bot_commands import set_default_commands
from utils.cache import TTLCache


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    settings = load_settings()
    await init_db()

    timeout = aiohttp.ClientTimeout(total=10)
    session = aiohttp.ClientSession(timeout=timeout)

    bot = Bot(token=settings.bot_token, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    dp["session"] = session
    dp["settings"] = settings
    dp["cache"] = TTLCache(max_items=512)

    for router in get_routers():
        dp.include_router(router)

    await set_default_commands(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
