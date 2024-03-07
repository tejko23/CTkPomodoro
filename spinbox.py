from typing import Callable, Union

import customtkinter

class Spinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs
                 ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = customtkinter.CTkButton(self, 
                                                       text="-", 
                                                       width=height-6, 
                                                       height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkLabel(self, 
                                            width=width-(2*height), 
                                            height=height-6)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, 
                                                  text="+", 
                                                  width=height-6, 
                                                  height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)
        self.entry.configure(text="25")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.cget("text"))  + self.step_size
            value = 60 if value > 60 else value
            self.entry.configure(text=value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.cget("text")) - self.step_size
            value = 5 if value < 5 else value
            self.entry.configure(text=value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.cget("text"))
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.configure(text=value)