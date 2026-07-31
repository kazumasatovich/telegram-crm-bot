import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError, TelegramUnauthorizedError

from crm_bot.config import load_config
from crm_bot.handlers import setup_handlers
from crm_bot.storage import RequestStorage


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    config = load_config()

    session = AiohttpSession()
    session.timeout = 60
    bot = Bot(token=config.bot_token, session=session)
    dp = Dispatcher()

    storage = RequestStorage()
    router = setup_handlers(storage, config)
    dp.include_router(router)

    try:
        me = await bot.get_me()
        logging.info("Bot started: @%s", me.username)
    except TelegramUnauthorizedError as e:
        logging.error("Bot token is invalid, check it on @BotFather: %s", e)
        await bot.session.close()
        sys.exit(1)
    except TelegramNetworkError as e:
        logging.error("Error connection to Telegram, check your network: %s", e)
        await bot.session.close()
        sys.exit(1)

    try:
        await dp.start_polling(bot)
    except TelegramNetworkError as e:
        logging.error("Network error (check the VPN): %s", e)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
