import os
import pathlib


from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions

BASE_DIR = pathlib.Path(__file__).parent.resolve()
os.environ["BASE_DIR"] = str(BASE_DIR)

from back.config_manager import get_config

from back.tg_items.keyboards_and_buttons import (
    set_reply_markup_keyboard,
    generate_keyboard,
    share_location_button,
    view_log_button,
)

set_reply_markup_keyboard(generate_keyboard(share_location_button, view_log_button))

from back.tg_items.security_layer import security_message_handlers
from back.tg_items.message_handlers import event_handlers_registry


CONFIG = get_config()
SECRETS = get_config(full_file_path=os.path.join(BASE_DIR, "misc", "secrets.json"))
ADMIN_TG_ID = SECRETS.get("ADMIN_TG_ID")
os.environ["ADMIN_TG_ID"] = ADMIN_TG_ID

print()


bot = Bot(token=SECRETS["TG_TOKEN"])
dp = Dispatcher(bot)

event_handler_list = []


event_handler_list += security_message_handlers
event_handler_list += event_handlers_registry

for event_handler_item in event_handler_list:
    dp.register_message_handler(
        event_handler_item["function"],
        commands=event_handler_item["commands"],
        content_types=event_handler_item["content_types"],
    )


if __name__ == "__main__":
    try:
        executor.start_polling(dp, skip_updates=True)
    except exceptions.TerminatedByOtherGetUpdates:
        pass
