import datetime
from typing import Callable, Optional, Union

import customtkinter


class Spinbox(customtkinter.CTkFrame):
    def __init__(
        self,
        *args,
        width: int = 100,
        height: int = 32,
        entry: str = "5",
        step_size: int = 1,
        min_value: int = 1,
        max_value: int = 60,
        command: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.min_value = min_value
        self.max_value = max_value
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = customtkinter.CTkButton(
            self,
            text="-",
            width=height - 6,
            height=height - 6,
            command=self.subtract_button_callback,
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkLabel(
            self, width=width - (2 * height), height=height - 6
        )
        self.entry.grid(
            row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew"
        )

        self.add_button = customtkinter.CTkButton(
            self,
            text="+",
            width=height - 6,
            height=height - 6,
            command=self.add_button_callback,
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.entry.configure(text=entry)

    def add_button_callback(self):
        try:
            value = int(self.entry.cget("text")) + self.step_size
            value = self.max_value if value > self.max_value else value
            self.entry.configure(text=str(value))
        except ValueError:
            raise ValueError
        else:
            if self.command is not None:
                self.command()

    def subtract_button_callback(self):
        try:
            value = int(self.entry.cget("text")) - self.step_size
            value = self.min_value if value < self.min_value else value
            self.entry.configure(text=str(value))
        except ValueError:
            raise ValueError
        else:
            if self.command is not None:
                self.command()

    def get(self) -> Union[str, None]:
        return self.entry.cget("text")
