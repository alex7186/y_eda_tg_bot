import os
import logging


def mprint(message: str) -> None:
    """it's like usual 'print' but with logging"""
    try:
        logging.info(message)

    except Exception as e:
        pass


if __name__ != "__main__":

    logging.basicConfig(
        filename=os.path.join(os.environ.get("BASE_DIR"), "misc", "logfile.txt"),
        filemode="a",
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
