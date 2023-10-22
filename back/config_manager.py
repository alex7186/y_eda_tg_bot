import json
import os


def get_config(full_file_path=None):

    if full_file_path:
        file_path = full_file_path
    else:
        file_path = os.path.join(os.environ.get("BASE_DIR"), "misc", "config.json")

    with open(file_path, "r") as f:
        data = f.read()
    return json.loads(data)


def set_config(config: dict, full_file_path=None):

    if full_file_path:
        file_path = full_file_path
    else:
        file_path = os.path.join(os.environ.get("BASE_DIR"), "misc", "config.json")

    with open(file_path, "w") as f:
        f.write(json.dumps(config, indent=4))
