import configparser
from typing import Optional


class ConfigManager:
    def __init__(self, path: Optional[str] = None):
        if path is None:
            self.path = "config.ini"
        else:
            self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(self.path)

    def save_param(self, key: str, value: str):
        self.config.read(self.path)
        self.config["Settings"][key] = value
        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def load_param(self, key: str):
        self.config.read(self.path)
        return self.config["Settings"][key]

    def get_pomodoro_time(self) -> str:
        self.config.read(self.path)
        return self.config["Settings"]["pomodoro_time"]
