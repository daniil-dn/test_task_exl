import aiogram
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from bot.filters.role import RoleFilter, AdminFilter
from bot.handles.admin import register_admin
from bot.handles.user import register_user
from bot.middlewares.db import DbMiddleware
from bot.middlewares.environment import EnvironmentMiddleware
from bot.middlewares.role import RoleMiddleware
from bot.config import load_config

logfile = 'log_bot.log'
info_log_file = "log_info.log"
config = load_config("bot/bot.ini")


async def on_startup(dp):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    err_handler = logging.FileHandler('log_errors.log')
    all_handler = logging.FileHandler('log_all.log')
    err_handler.setLevel(logging.ERROR)
    all_handler.setLevel(logging.DEBUG)
    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    err_handler.setFormatter(c_format)
    all_handler.setFormatter(f_format)
    # Add handlers to the logger
    logger.addHandler(err_handler)
    logger.addHandler(all_handler)
    logger.error('Starting bot')

    # pool = await create_pool(
    #     user=config.db.user,
    #     password=config.db.password,
    #     database=config.db.database,
    #     host=config.db.host,
    #     echo=False,
    # )
    engine = create_engine("sqlite:///sql.db")
    pool_session = sessionmaker(
        engine, expire_on_commit=False
    )

    dp.middleware.setup(DbMiddleware(pool_session, logger))
    dp.middleware.setup(EnvironmentMiddleware(config, logger))
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_ids))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    register_admin(dp)
    register_user(dp)


if __name__ == '__main__':
    token = load_config('bot/bot.ini').tg_bot.token
    bot = aiogram.Bot(token=token)
    dp = aiogram.Dispatcher(bot=bot, storage=RedisStorage2())
    aiogram.executor.start_polling(dp, on_startup=on_startup)
