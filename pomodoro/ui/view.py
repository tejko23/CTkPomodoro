from tkinter import ttk
from typing import Callable

import customtkinter

from .settings import SettingsWindow


class Pomodoro(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro")
        self.geometry("400x400")

    def init_ui(self, config, time):
        self.job = None
        self.config = config
        self.grid_columnconfigure((0, 1), weight=1)

        self.header_frame = AppHeaderFrame(
            self, command=self.open_settings_window
        )
        self.header_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2
        )

        self.update_btn = customtkinter.CTkButton(self, text="Reload time")
        self.update_btn.grid(
            row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2
        )

        self.clock = ClockFrame(self, time=time)
        self.clock.grid(
            row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2
        )

        self.button_command: Callable = self.swap_button_text_decorator
        self.button = customtkinter.CTkButton(
            self, text="Start", command=self.button_command
        )
        self.button.grid(
            row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=2
        )
        self.settings_window = None

    def set_clock_label(self, time: str) -> None:
        self.clock.time = time

    def bind_update_button(self, fn: Callable) -> None:
        self.update_btn.configure(command=fn)

    def bind_ss_button(self, fn: Callable) -> None:
        self.button_command = lambda: self.swap_button_text_decorator(
            command=fn
        )
        self.button.configure(command=self.button_command)

    def swap_button_text_decorator(self, command=None, *args, **kwargs):
        def wrapper(*args, **kwargs):
            if self.button.cget("text") == "Start":
                self.button.configure(text="Stop")
                self.update_btn.configure(state="disabled")
            else:
                self.button.configure(text="Start")
                self.update_btn.configure(state="normal")
            return command() if command is not None else None

        return wrapper()

    def run_job(self, time_ms, func, *args):
        self.job = self.after(time_ms, func, *args)

    def cancel_job(self):
        self.after_cancel(self.job)

    def open_settings_window(self):
        """
        Open settings window.
        """
        if (
            self.settings_window is None
            or not self.settings_window.winfo_exists()
        ):
            self.settings_window = SettingsWindow(self, self.config)
        else:
            self.settings_window.focus()


class AppHeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, command):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(
            self, text="Pomodoro", font=customtkinter.CTkFont(size=30)
        )
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.settings_btn = customtkinter.CTkButton(
            self, text="Settings", command=command
        )
        self.settings_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.divider = ttk.Separator(self, orient="horizontal")
        self.divider.grid(
            row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2
        )


class ClockFrame(customtkinter.CTkFrame):
    def __init__(self, master, time: str = "10:00"):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(
            self, font=customtkinter.CTkFont(size=50), text=time
        )
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    @property
    def time(self) -> str:
        return self.label.cget("text")

    @time.setter
    def time(self, value: str):
        self.label.configure(text=value)
