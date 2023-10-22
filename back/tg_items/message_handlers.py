from datetime import datetime

from aiogram.types import Message
from aiogram.utils import exceptions

from back.sqlite3_manager import calculate_distance, add_log
from back.df_viewing_manager import make_md_text
from back.tg_items.keyboards_and_buttons import reply_markup_keyboard


async def show_start(message: Message):

    await user_sends_location(message)


async def user_sends_location(message: Message):
    global reply_markup_keyboard

    await message.answer(
        "Нажмите на кнопку ниже чтобы поделиться своей геолокацией",
        reply_markup=reply_markup_keyboard,
    )


async def cmd_locate_me(message: Message):
    global reply_markup_keyboard

    add_log(
        date_str=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        user_tg_id=str(message.from_id),
        location_longitude=message.location.longitude,
        location_latitude=message.location.latitude,
    )

    try:
        await message.answer(
            text=make_md_text(
                calculate_distance(
                    message.location.latitude,
                    message.location.longitude,
                    result_count=10,
                )
            ),
            reply_markup=reply_markup_keyboard,
        )

    except exceptions.MessageTextIsEmpty:
        await message.answer(text="Внутреняя ошибка")


event_handlers_registry = [
    {"function": show_start, "commands": None, "content_types": None},
    {"function": user_sends_location, "commands": ["locate_me"], "content_types": None},
    {"function": cmd_locate_me, "commands": None, "content_types": ["location"]},
]
