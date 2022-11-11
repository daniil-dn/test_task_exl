import asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.engine.url import URL

from bot.config import load_config

config = load_config("bot/bot.ini")


def main():
    # Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    # engine = create_engine(URL.create(**DATABASE))
    engine = create_engine("sqlite:///sql.db")
    from models.schemas import Base
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



if __name__ == "__main__":
    main()
