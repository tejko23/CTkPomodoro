from tkinter import ttk

import customtkinter

from settings import SettingsWindow, ConfigManager
from timer import TimeCounter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro")
        self.geometry("400x400")
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.timer = TimeCounter(ConfigManager().load_param("pomodoro_time"))

        self.header_frame = AppHeaderFrame(self)
        self.header_frame.grid(row=0,
                               column=0,
                               padx=10,
                               pady=10,
                               sticky='ew',
                               columnspan=2)
        
        self.update_btn = customtkinter.CTkButton(self, 
                                              text="Reload time", 
                                              command=self.set_time)
        self.update_btn.grid(row=1, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.clock = ClockFrame(self, time=self.timer)
        self.clock.grid(row=2,
                        column=0,
                        padx=20,
                        pady=20,
                        sticky='ew',
                        columnspan=2)
        
        self.button = customtkinter.CTkButton(self, 
                                              text="Start", 
                                              command=self.manage)
        self.button.grid(row=3, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)

    def set_time(self):
        self.timer.time = ConfigManager().load_param("pomodoro_time")
        self.clock.time = self.timer

    def manage(self):
        if not self.timer.is_running:
            if self.timer.is_finished:
                self.set_time()
            self.timer.toggle()
            self.button.configure(text="Stop")
            self.pomodoro()
        else:
            self.timer.toggle()
            self.button.configure(text="Start")

    def pomodoro(self):
        if self.timer.is_running:
            sleep = 200
            self.clock.time = self.timer
            if self.timer.is_finished:
                sleep = 1000
                self.bell()
            self.after(sleep, self.pomodoro)


class AppHeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master,
                         fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)

        self.settings_window = None

        self.label = customtkinter.CTkLabel(self, text="Pomodoro", 
                                            font=customtkinter.CTkFont(
                                                size=30
                                                ))
        self.label.grid(row=0, 
                        column=0, 
                        padx=10, 
                        pady=10, 
                        sticky='w')
        
        self.settings_btn = customtkinter.CTkButton(self,
                                                text="Settings",
                                                command=self.open_settings)
        self.settings_btn.grid(row=0, 
                               column=1, 
                               padx=10, 
                               pady=10, 
                               sticky="e")
        
        self.divider = ttk.Separator(self, orient="horizontal")
        self.divider.grid(row=1, 
                          column=0, 
                          padx=10, 
                          pady=10, 
                          sticky="ew",
                          columnspan=2)
    
    def open_settings(self):
        """
        Open settings window
        """
        if self.settings_window is None \
                or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus()


class ClockFrame(customtkinter.CTkFrame):
    def __init__(self, master, 
                 time: str = "10:00"):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.label = customtkinter.CTkLabel(self,  
                                            font=customtkinter.CTkFont(
                                                size=50
                                            ),
                                            text=time)
        self.label.grid(row=0, 
                        column=0, 
                        padx=10, 
                        pady=10, 
                        sticky="ew")
        
    @property
    def time(self) -> str:
        return self.label.cget("text")
    
    @time.setter
    def time(self, value: str):
        self.label.configure(text=value)


if __name__ == '__main__':
    app = App()
    app.mainloop()