import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    bot_token: str
    manager_ids: list[int]


def load_config() -> Config:
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN не найдет в .env")

    raw_ids = os.getenv("MANAGER_IDS", "")
    manager_ids = [int(i) for i in raw_ids.split(",") if i.strip()]

    return Config(bot_token=token, managers_ids=manager_ids)
