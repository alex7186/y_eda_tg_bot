import os
import random

import pandas as pd

from io import BytesIO
from tabulate import tabulate
from PIL import ImageDraw


def make_md_text(input_df: pd.DataFrame) -> str:

    text = ""

    for _, row in input_df.iterrows():

        # printing address
        text = text + "{} {} п{}".format(
            row["address_street"],
            row["address_house"],
            row["address_entrance"],
        )

        # printing domophone codes
        for code_element in (
            row["codes_list"].casefold().replace("\n", " ").replace("код", "").split()
        ):

            # printing only if contains numbers
            if any(char.isdigit() for char in code_element):
                text = text + "\n   {}".format(code_element)

        text = text + "\n\n"

    return text[:-2]


def any_make_md_text(input_df: pd.DataFrame, columns: list[str]) -> str:

    return tabulate(input_df, headers=columns, showindex=False)


def make_timetable_image_buff(input_df, font, background_image):
    class TextImage:
        def __init__(self, timetable_text, font, background_image):

            self.timetable_text = timetable_text
            self.background_image = background_image
            self.font = font

        def crop_image(self, img, new_w, new_h):
            w, h = img.size

            return img.crop(
                ((w - new_w) / 2, (h - new_h) / 2, (w + new_w) / 2, (h + new_h) / 2)
            )

        def make_timetable_image(
            self,
            image_size,
            color=(255, 255, 255),
        ):

            self.background_image = (
                self.crop_image(self.background_image, *image_size)
            ).point(lambda pixel: pixel * 0.5)

            drawer = ImageDraw.Draw(self.background_image)
            drawer.multiline_text(
                (15, 15),
                self.timetable_text,
                fill=color,
                font=self.font,
            )

            return self.background_image

    table_text = tabulate(
        input_df, headers=["date", "tg_id", "lon", "lat"], showindex=False
    )

    lines_count = len(table_text.split("\n"))
    line_max_len = 0
    for line in table_text.split("\n"):
        if len(line) > line_max_len:
            line_max_len = len(line)

    image_size = (30 + 9 * line_max_len, 30 + 18 * lines_count)

    buff = BytesIO()

    TextImage(
        timetable_text=table_text,
        font=font,
        background_image=background_image,
    ).make_timetable_image(image_size).save(buff, format="PNG")

    return buff.getvalue()


def pick_background_image_path(CURR_PATH):

    random_image_filename = random.choice(os.listdir(CURR_PATH))
    background_image_path = os.path.join(CURR_PATH, random_image_filename)

    return background_image_path
