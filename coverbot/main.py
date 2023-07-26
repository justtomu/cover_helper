import asyncio
import os
import threading
import time
from sys import argv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand
from aiogram.utils import executor

from handlers.command import handlers as cover_handlers
from handlers.callback import handlers as callback_handlers
from handlers.message import handlers as text_handlers
from utils import config
from text import t
from utils.log import log
from aiogram.contrib.middlewares.logging import LoggingMiddleware


async def on_startup(dispatcher):
    await dispatcher.bot.set_my_commands([BotCommand('start', 'Restart bot')])


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def main():
    log.info('Starting bot...')
    log.info(f'Pid is {str(os.getpid())}')
    bot = Bot(token=config.BOT_TOKEN)
    storage = RedisStorage2(config.REDIS_HOST, port=int(config.REDIS_PORT), db=3, password=None)
    dp = Dispatcher(bot, storage=storage)
    cover_handlers.apply_to_dispatcher(dp)
    callback_handlers.apply_to_dispatcher(dp)
    text_handlers.apply_to_dispatcher(dp)
    t.load_translations('cover_bot')

    executor.start_polling(dp, timeout=0, skip_updates=True, on_shutdown=on_shutdown, on_startup=on_startup)


if __name__ == '__main__':
    main()
