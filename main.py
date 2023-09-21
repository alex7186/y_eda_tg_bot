import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from back.config_manager import get_config
from back.sqlite3_manager import sqlite3_manager_init
from back.config_manager import get_config

from back.tg_items.message_handlers import event_handlers_registry
from back.tg_items.security_layer import security_message_handlers


BASE_DIR = os.getcwd()
CONFIG = get_config(BASE_DIR=BASE_DIR)
SECRETS = get_config(full_file_path=os.path.join(BASE_DIR, "misc", "secrets.json"))

sqlite3_manager_init(BASE_DIR=BASE_DIR)


bot = Bot(token=SECRETS["TG_TOKEN"])
dp = Dispatcher(bot)


for event_handler_item in [*event_handlers_registry, *security_message_handlers]:
    dp.register_message_handler(
        event_handler_item["function"],
        commands=event_handler_item["commands"],
        content_types=event_handler_item["content_types"],
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
