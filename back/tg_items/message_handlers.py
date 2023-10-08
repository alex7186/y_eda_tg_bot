from datetime import datetime

from aiogram.types import Message
from aiogram.utils import exceptions

from back.sqlite3_manager import calculate_distance, add_log
from back.df_viewing_manager import make_md_text
from back.tg_items.keyboards_and_buttons import share_location_button, generate_keyboard


async def show_start(message: Message):

    await user_sends_location(message)


async def user_sends_location(message: Message):
    reply = "Нажмите на кнопку ниже чтобы поделиться своей геолокацией"
    await message.answer(
        reply,
        reply_markup=generate_keyboard(
            share_location_button,
        ),
    )


async def cmd_locate_me(message: Message):

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
            reply_markup=generate_keyboard(
                share_location_button,
            ),
        )

    except exceptions.MessageTextIsEmpty:
        await message.answer(text="Внутреняя ошибка")


event_handlers_registry = [
    {"function": show_start, "commands": None, "content_types": None},
    {"function": user_sends_location, "commands": ["locate_me"], "content_types": None},
    {"function": cmd_locate_me, "commands": None, "content_types": ["location"]},
]
