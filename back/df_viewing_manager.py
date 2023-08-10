import pandas as pd


def make_md_text(input_df: pd.DataFrame) -> str:

    text = ""

    for i, row in input_df.iterrows():

        row_distance = int(row["distance"] * 1000)
        if row_distance == 0:
            continue

        # printing address
        text = text + "{} {} п{} ({}м)".format(
            row["address_street"],
            row["address_house"],
            row["address_entrance"],
            row_distance,
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


# def clear_df(input_df: pd.DataFrame) -> pd.DataFrame:
#     input_df = input_df[input_df["distance"] > 0]

#     return input_df["distance"].apply(lambda x: x*1000)


