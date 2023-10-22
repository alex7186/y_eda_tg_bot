from aiogram import types


reply_markup_keyboard = None

share_location_button = types.KeyboardButton(
    "Поделиться геолокацией 🗺️📍", request_location=True
)

view_log_button = types.KeyboardButton("Показать логи 📁")


def generate_keyboard(*buttons):
    return types.ReplyKeyboardMarkup(
        keyboard=[[element] for element in buttons],
        resize_keyboard=True,
    )


def set_reply_markup_keyboard(
    input_reply_markup_keyboard: types.ReplyKeyboardMarkup,
) -> None:
    global reply_markup_keyboard

    reply_markup_keyboard = input_reply_markup_keyboard
