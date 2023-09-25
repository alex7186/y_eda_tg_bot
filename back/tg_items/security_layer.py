import os

from dataclasses import dataclass


from back.df_viewing_manager import make_timetable_image_buff
from aiogram.types import Message

from back.sqlite3_manager import read_logs_stat, clear_self_logs

# from back.tg_items.keyboards_and_buttons import share_location_button, generate_keyboarde

local_secrets = None


# TODO rewrite rights checking logic

# @dataclass
# class SecurityContext:
#     # throw exception if whitelist required and user_id not in white list

#     func_for_administration: bool = False
#     users_id_list: list[str] | None = None

#     def check(self, current_user_id: str = None):
#         if self.func_for_administration and self.users_id_list != None:
#             if current_user_id not in self.users_id_list:
#                 return False
#         return True


async def proc_clear_self_logs(message: Message):
    global local_secrets
    global font
    global background_image

    if str(message.from_id) not in local_secrets["WHITE_LIST"]:
        await message.answer(text="Внутреняя ошибка ")
        return None

    clear_self_logs()

    await message.answer("Самоданные отчищены")


async def view_log(message: Message):
    global local_secrets
    global font
    global background_image

    if str(message.from_id) not in local_secrets["WHITE_LIST"]:
        await message.answer(text="Внутреняя ошибка ")
        return None

    await message.reply_photo(
        make_timetable_image_buff(
            input_df=read_logs_stat(n_max=20),
            font=font,
            background_image=background_image,
        )
    )


security_message_handlers = [
    {
        "function": proc_clear_self_logs,
        "commands": ["clear_self_logs"],
        "content_types": None,
    },
    {"function": view_log, "commands": ["view_usage_logs"], "content_types": None},
]
