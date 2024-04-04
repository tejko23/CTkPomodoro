import configparser


class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def save_param(self, key: str, value: str):
        self.config["Settings"][key] = value
        with open("config.ini", "w") as config_file:
            self.config.write(config_file)

    def load_param(self, key: str):
        return self.config["Settings"][key]

    def get_pomodoro_time(self) -> str:
        return self.config["Settings"]["pomodoro_time"]
