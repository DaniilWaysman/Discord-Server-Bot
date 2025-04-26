import json

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def save_config(data):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

config_data = load_config()
PREFIX = config_data["PREFIX"]
OWNER_ID = config_data["OWNER_ID"]
