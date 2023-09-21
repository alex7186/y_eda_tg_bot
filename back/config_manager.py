import json
import os


def get_config(BASE_DIR=None, full_file_path=None):
    if not full_file_path:
        PATH = os.path.join(BASE_DIR, "misc", "config.json")
    else:
        PATH = full_file_path
    with open(PATH, "r") as f:
        data = f.read()
    return json.loads(data)


def set_config(config: dict, BASE_DIR=None, full_file_path=None):
    if not full_file_path:
        PATH = os.path.join(BASE_DIR, "misc", "config.json")
    else:
        PATH = full_file_path
    with open(PATH, "w") as f:
        f.write(json.dumps(config, indent=4))
