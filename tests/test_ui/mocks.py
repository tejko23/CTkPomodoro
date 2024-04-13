import customtkinter
from pomodoro.ui.view import SettingsWindowFactory


class AppMock(customtkinter.CTk):
    def __init__(self):
        super().__init__()


class SettingsWindowMock:
    def __init__(self, master, config, *args, **kwargs):
        pass

    def winfo_exists(self):
        return True

    def focus(self):
        return "Mocked window focused"


class ClockMock:
    def __init__(self, master, time: str = "10:00") -> None:
        self.time = time


class ButtonMock:
    def __init__(self) -> None:
        self.text = "Start"

    def configure(self, require_redraw=False, **kwargs):
        if "text" in kwargs:
            self.text = kwargs.pop("text")

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self.text
