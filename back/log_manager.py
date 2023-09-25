import os
import logging

LOG_INITIALIZED = False


def log_init(BASE_DIR=None, full_file_path=None):

    file_path = None

    file_path = (
        os.path.join(BASE_DIR, "misc", "logfile.txt") if BASE_DIR else full_file_path
    )

    logging.basicConfig(
        filename=file_path,
        filemode="a",
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )


def mprint(message: str) -> None:
    """it's like usual 'print' but with logging"""
    try:
        logging.info(message)

    except Exception as e:
        pass
