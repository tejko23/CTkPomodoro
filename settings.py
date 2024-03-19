import configparser
from typing import Union
from tkinter import ttk

import customtkinter

from spinbox import Spinbox

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def save_param(self, key: str, value: str):
        self.config['Settings'][key] = value
        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)

    def load_param(self, key: str):
        return self.config['Settings'][key]


class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Settings")
        self.geometry("400x300")
        self.config = ConfigManager()

        self.attributes("-topmost", True)

        self.columnconfigure((0, 1), weight=1)

        self.label = customtkinter.CTkLabel(self, 
                                        text="Settings",
                                        font=customtkinter.CTkFont(size=26))
        self.label.grid(row=0, 
                        column=0, 
                        padx=20, 
                        pady=20, 
                        sticky="ew", 
                        columnspan=2)

        self.divider = ttk.Separator(self, orient="horizontal")
        self.divider.grid(row=1, 
                          column=0, 
                          padx=10, 
                          pady=10, 
                          sticky="ew", 
                          columnspan=2)
        

        self.label = customtkinter.CTkLabel(self, 
                                        text="Pomodoro time: ")
        self.label.grid(row=2, 
                        column=0, 
                        padx=20, 
                        pady=20, 
                        sticky="w", 
                        columnspan=2)
        
        self.pomodoro_time = Spinbox(self, 
                                     entry=self.config.load_param("pomodoro_time"), 
                                     step_size=1, 
                                     command=self._save_to_config)
        self.pomodoro_time.grid(row=2, 
                                column=1, 
                                padx=20, 
                                pady=20, 
                                sticky="ew", 
                                columnspan=2)
        
    def _save_to_config(self):
        self.config.save_param('pomodoro_time', self.get())
        
    def get(self) -> Union[int, None]:
        return self.pomodoro_time.get()