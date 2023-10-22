import os
from tabulate import tabulate

from aiogram.types import Message

from back.sqlite3_manager import read_logs_stat, clear_self_logs
from back.tg_items.keyboards_and_buttons import reply_markup_keyboard


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


ADMIN_TG_ID = os.environ.get("ADMIN_TG_ID")


async def view_log(message: Message):
    global ADMIN_TG_ID

    if str(message.from_id) != ADMIN_TG_ID and False:
        await message.answer(text="Внутреняя ошибка ")
        return None

    clear_self_logs()

    await message.answer(
        text=tabulate(
            read_logs_stat(n_max=20),
            # headers=["date", "tg_id", "geo"],
            headers="keys",
        ),
        parse_mode="MarkdownV2",
        disable_web_page_preview=True,
        reply_markup=reply_markup_keyboard,
    )


security_message_handlers = [
    # {"function": view_log, "commands": ["view_usage_logs"], "content_types": None},
    {"function": view_log, "commands": None, "content_types": None},
]
