from typing import Protocol
from tkinter import ttk

import customtkinter

from .spinbox import Spinbox


class Config(Protocol):
    def get_pomodoro_time(self) -> str: ...
    def get_break_time(self) -> str: ...
    def get_long_break_time(self) -> str: ...
    def get_long_break_interval(self) -> str: ...
    def set_long_break_interval(self, value: str) -> None: ...


class Presenter(Protocol):
    def set_sequence_interval(self, value: str) -> None: ...


class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(
        self, master, presenter: Presenter, config: Config, *args, **kwargs
    ):
        super().__init__(master, *args, **kwargs)
        self.title("Settings")
        self.geometry("400x400")

        self.attributes("-topmost", True)

        self.columnconfigure((0, 1), weight=1)

        self.presenter = presenter
        self.config = config

        self.label = customtkinter.CTkLabel(
            self, text="Settings", font=customtkinter.CTkFont(size=26)
        )
        self.label.grid(
            row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2
        )

        self.divider = ttk.Separator(self, orient="horizontal")
        self.divider.grid(
            row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2
        )

        self.pomodoro_label = customtkinter.CTkLabel(
            self, text="Pomodoro time: "
        )
        self.pomodoro_label.grid(
            row=2, column=0, padx=20, pady=10, sticky="w", columnspan=2
        )

        self.pomodoro_time = Spinbox(
            self,
            entry=self.config.get_pomodoro_time(),
            step_size=1,
            command=lambda: self._save_to_config("pomodoro_time"),
        )
        self.pomodoro_time.grid(
            row=2, column=1, padx=20, pady=10, sticky="ew", columnspan=2
        )

        self.break_label = customtkinter.CTkLabel(self, text="Break time: ")
        self.break_label.grid(
            row=3, column=0, padx=20, pady=10, sticky="w", columnspan=2
        )

        self.break_time = Spinbox(
            self,
            entry=self.config.get_break_time(),
            step_size=1,
            command=lambda: self._save_to_config("break_time"),
        )
        self.break_time.grid(
            row=3, column=1, padx=20, pady=10, sticky="ew", columnspan=2
        )

        self.long_break_label = customtkinter.CTkLabel(
            self, text="Long break time: "
        )
        self.long_break_label.grid(
            row=4, column=0, padx=20, pady=10, sticky="w", columnspan=2
        )

        self.long_break_time = Spinbox(
            self,
            entry=self.config.get_long_break_time(),
            step_size=1,
            command=lambda: self._save_to_config("long_break_time"),
        )
        self.long_break_time.grid(
            row=4, column=1, padx=20, pady=10, sticky="ew", columnspan=2
        )

        self.long_break_interval_label = customtkinter.CTkLabel(
            self, text="Long break interval: "
        )
        self.long_break_interval_label.grid(
            row=5, column=0, padx=20, pady=10, sticky="w", columnspan=2
        )

        self.long_break_interval = Spinbox(
            self,
            entry=self.config.get_long_break_interval(),
            min_value=2,
            max_value=5,
            step_size=1,
            command=self._set_interval,
        )
        self.long_break_interval.grid(
            row=5, column=1, padx=20, pady=10, sticky="ew", columnspan=2
        )

    def _save_to_config(self, type: str):
        value = getattr(self, f"{type}").get()
        getattr(self.config, f"set_{type}")(value)

    def _set_interval(self):
        value = self.long_break_interval.get()
        self.config.set_long_break_interval(value)
        self.presenter.set_sequence_interval(value)
