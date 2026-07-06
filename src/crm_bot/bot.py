import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError

from crm_bot.config import load_config
from crm_bot.handlers import setup_handlers
from crm_bot.storage import RequestStorage


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = load_config()

    session = AiohttpSession()
    session.timeout = 60
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    storage = RequestStorage()
    router = setup_handlers(storage, config)
    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except TelegramNetworkError as e:
        logging.error("Сетевая ошибка (Проверьте VPN): %s", e)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
