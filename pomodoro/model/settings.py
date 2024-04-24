import configparser
from typing import Optional


class ConfigManager:
    def __init__(self, path: Optional[str] = None):
        self.path = path or "config.ini"
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self) -> None:
        self.config.read(self.path)

    def _save_config(self) -> None:
        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def _set_param(self, key: str, value: str) -> None:
        self._load_config()
        self.config["Settings"][key] = value
        self._save_config()

    def _get_param(self, key: str) -> str:
        self._load_config()
        return self.config["Settings"][key]

    def get_pomodoro_time(self) -> str:
        return self._get_param("pomodoro_time")

    def set_pomodoro_time(self, value: str) -> None:
        self._set_param("pomodoro_time", value)

    def get_break_time(self) -> str:
        return self._get_param("break_time")

    def set_break_time(self, value: str) -> None:
        self._set_param("break_time", value)

    def get_long_break_time(self) -> str:
        return self._get_param("long_break_time")

    def set_long_break_time(self, value: str) -> None:
        self._set_param("long_break_time", value)

    def get_long_break_interval(self) -> str:
        return self._get_param("long_break_interval")

    def set_long_break_interval(self, value: str) -> None:
        self._set_param("long_break_interval", value)
