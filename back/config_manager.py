import json


def get_config(SCRIPT_PATH=None, full_file_path=None):
    if not full_file_path:
        PATH = f"{SCRIPT_PATH}/misc/config.json"
    else:
        PATH = full_file_path
    with open(PATH, "r") as f:
        data = f.read()
    return json.loads(data)


def set_config(config: dict, SCRIPT_PATH=None, full_file_path=None):
    if not full_file_path:
        PATH = f"{SCRIPT_PATH}/misc/config.json"
    else:
        PATH = full_file_path
    with open(PATH, "w") as f:
        f.write(json.dumps(config, indent=4))
