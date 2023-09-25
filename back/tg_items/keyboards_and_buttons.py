from aiogram import types


share_location_button = types.KeyboardButton(
    "Поделиться геолокацией 🗺️📍", request_location=True
)

view_log_button = types.KeyboardButton("Показать логи")


def generate_keyboard(*buttons):
    return types.ReplyKeyboardMarkup(
        keyboard=[[element] for element in buttons],
        resize_keyboard=True,
    )


# @dp.callback_query_handler('btn5')
# async def process_callback_kb1btn1(callback_query: types.CallbackQuery):

#     await bot.send_message(callback_query.from_user.id,
#         f'Нажата инлайн кнопка! code')
