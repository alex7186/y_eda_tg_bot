import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from back.config_manager import get_config
from back.sqlite3_manager import sqlite3_manager_init
from back.log_manager import log_init, mprint

from back.tg_items.message_handlers import event_handlers_registry


# BASE_DIR = os.getcwd()
BASE_DIR = os.path.abspath("/media/alex/drive_2tb/y_eda_tg_bot")
CONFIG = get_config(BASE_DIR=BASE_DIR)
SECRETS = get_config(full_file_path=os.path.join(BASE_DIR, "misc", "secrets.json"))

bot = Bot(token=SECRETS["TG_TOKEN"])
dp = Dispatcher(bot)

event_handler_list = []


sqlite3_manager_init(BASE_DIR=BASE_DIR)
log_init(BASE_DIR=BASE_DIR)

mprint(BASE_DIR)
if int(CONFIG["SECURITY"]) == 1:
    from PIL import Image, ImageFont

    from back.tg_items.security_layer import security_message_handlers
    from back.df_viewing_manager import pick_background_image_path

    background_image = Image.open(
        pick_background_image_path(os.path.join(BASE_DIR, "misc", "img", "images"))
    )

    font = ImageFont.truetype(
        os.path.join(BASE_DIR, "misc", "img", "fonts", "RobotoMono-Medium.ttf"), size=15
    )

    # TODO export BASE_DIR, background_image, font as variables (exposed), CONFIG,
    # TODO rename background_image, font vars


if int(CONFIG["SECURITY"]) == 1:
    event_handler_list += security_message_handlers

event_handler_list += event_handlers_registry

for event_handler_item in event_handler_list:
    dp.register_message_handler(
        event_handler_item["function"],
        commands=event_handler_item["commands"],
        content_types=event_handler_item["content_types"],
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
