import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions

from back.log_manager import log_init, mprint
from back.postgresql_manager import calculate_distance
from back.df_viewing_manager import make_md_text


BASE_DIR = os.getcwd()
TG_TOKEN = "5096267040:AAFa_d_YJHhVCxhw44xUlEqG_ypqTUSMcsg"

log_init(os.path.join(BASE_DIR, "misc", "log.txt"))

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)


share_location_button = types.KeyboardButton(
    "Поделиться геолокацией 🗺️📍", request_location=True
)


def generate_keyboard(*buttons):
    return types.ReplyKeyboardMarkup(
        keyboard=[[element] for element in buttons],
        resize_keyboard=True,
    )


@dp.message_handler()
async def show_start(message: types.Message):

    mprint(f"{message.from_id} messaged")

    await user_sends_location(message)


@dp.message_handler(commands=["locate_me"])
async def user_sends_location(message: types.Message):
    reply = "Нажмите на кнопку ниже чтобы поделиться своей геолокацией"
    await message.answer(reply, reply_markup=generate_keyboard(share_location_button))


@dp.message_handler(content_types=["location"])
async def cmd_locate_me(message: types.Message):

    mprint(
        f"{message.from_id} searching {message.location.latitude} {message.location.longitude}"
    )

    try:
        await bot.send_message(
            chat_id=message.from_id,
            text=make_md_text(
                calculate_distance(
                    message.location.latitude,
                    message.location.longitude,
                    result_count=10,
                )
            ),
            reply_markup=generate_keyboard(share_location_button),
        )
        mprint(f"{message.from_id} sended successfully")

    except exceptions.MessageTextIsEmpty:
        await bot.send_message(chat_id=message.from_id, text="Внутреняя ошибка")
        mprint(f"{message.from_id} error")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
