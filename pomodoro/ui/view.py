from __future__ import annotations
from tkinter import ttk
from typing import Any, Callable, Optional, Protocol, Type

import customtkinter

from .settings import SettingsWindow


class SettingsWindowFactory:
    def __init__(
        self,
        settings_window_class: Optional[Type[SettingsWindow]] = None,
    ):
        self.settings_window_class = settings_window_class or SettingsWindow

    def create_settings_window(self, master, config):
        return self.settings_window_class(master, config)


class Config(Protocol):
    pass


class Pomodoro(customtkinter.CTk):
    def __init__(
        self, settings_window_factory: Optional[SettingsWindowFactory] = None
    ):
        super().__init__()

        self.title("Pomodoro")
        self.geometry("400x400")

        self.settings_window_factory = (
            settings_window_factory or SettingsWindowFactory()
        )

        self.job = None
        self.config: Config = None
        self.header_frame: Optional[AppHeaderFrame] = None
        self.pomodoro_time_btn: Optional[customtkinter.CTkButton] = None
        self.break_time_btn: Optional[customtkinter.CTkButton] = None
        self.long_break_time_btn: Optional[customtkinter.CTkButton] = None
        self.clock: Optional[ClockFrame] = None
        self.button_command: Optional[Callable[[], Any]] = None
        self.button: Optional[customtkinter.CTkButton] = None
        self.settings_window: Optional[SettingsWindow] = None

    def init_ui(self, config: Config, time: str) -> None:
        self.config = config
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.header_frame = AppHeaderFrame(
            self, command=self.open_settings_window
        )
        self.header_frame.grid(
            row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=3
        )

        self.pomodoro_time_btn = customtkinter.CTkButton(self, text="Pomodoro")
        self.pomodoro_time_btn.grid(
            row=1, column=0, padx=(20, 10), pady=10, sticky="ew", columnspan=1
        )

        self.break_time_btn = customtkinter.CTkButton(self, text="Break")
        self.break_time_btn.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=1
        )

        self.long_break_time_btn = customtkinter.CTkButton(
            self, text="Long break"
        )
        self.long_break_time_btn.grid(
            row=1, column=2, padx=(10, 20), pady=10, sticky="ew", columnspan=1
        )

        self.clock = ClockFrame(self, time=time)
        self.clock.grid(
            row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=3
        )

        self.button_command = self.swap_button_text_decorator
        self.button = customtkinter.CTkButton(
            self, text="Start", command=self.button_command
        )
        self.button.grid(
            row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=3
        )

    def set_clock_label(self, time: str) -> None:
        if self.clock is not None:
            self.clock.time = time
        else:
            raise TypeError("NoneType")

    def bind_button(self, time_type: str, command: Callable) -> None:
        if not callable(command):
            raise TypeError("'command' must be callable.")
        try:
            getattr(self, f"{time_type}_time_btn").configure(command=command)
        except Exception as e:
            raise AttributeError from e

    def bind_ss_button(self, command: Callable) -> None:
        if not callable(command):
            raise TypeError("'command' must be callable.")
        self.button_command = lambda: self.swap_button_text_decorator(
            command=command
        )
        if self.button is not None:
            self.button.configure(command=self.button_command)
        else:
            raise TypeError("NoneType")

    def swap_button_text_decorator(
        self, command: Optional[Callable] = None, *args, **kwargs
    ):
        def wrapper(*args, **kwargs):
            if self.button.cget("text") == "Start":
                self.button.configure(text="Stop")
                self._set_buttons_state(state="disabled")
            else:
                self.button.configure(text="Start")
                self._set_buttons_state(state="normal")
            return command() if command is not None else None

        return wrapper()

    def run_job(self, time_ms: int, func: Callable, *args):
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
            self.settings_window = (
                self.settings_window_factory.create_settings_window(
                    master=self,
                    config=self.config,
                )
            )
        else:
            self.settings_window.focus()

    def _set_buttons_state(self, state: str) -> None:
        self.pomodoro_time_btn.configure(state=state)
        self.break_time_btn.configure(state=state)
        self.long_break_time_btn.configure(state=state)


class AppHeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, command: Callable):
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
