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
        self.settings_window = None

        self.label = customtkinter.CTkLabel(self, text="Pomodoro", 
                                            font=customtkinter.CTkFont(
                                                size=30
                                                ))
        self.label.grid(row=0, 
                        column=0, 
                        padx=20, 
                        pady=20, 
                        sticky='w', 
                        columnspan=2)
        
        self.settings_btn = customtkinter.CTkButton(self,
                                                text="Settings",
                                                command=self.open_settings)
        self.settings_btn.grid(row=0, 
                               column=1, 
                               padx=20, 
                               pady=20, 
                               sticky="e", 
                               columnspan=2)
        
        self.divider = ttk.Separator(self, orient="horizontal")
        self.divider.grid(row=1, 
                          column=0, 
                          padx=10, 
                          pady=10, 
                          sticky="ew", 
                          columnspan=2)
        
        self.update_btn = customtkinter.CTkButton(self, 
                                              text="Reload time", 
                                              command=self.set_time)
        self.update_btn.grid(row=2, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.timer_label = customtkinter.CTkLabel(self,  
                                            font=customtkinter.CTkFont(
                                                size=50
                                                ))
        self.timer_label.grid(row=3, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.button = customtkinter.CTkButton(self, 
                                              text="Start", 
                                              command=self.manage)
        self.button.grid(row=4, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.timer = TimeCounter(ConfigManager().load_param("pomodoro_time"))
        
        self.refresh_timer_label()

    def open_settings(self):
        """
        Open settings window
        """
        if self.settings_window is None \
                or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus()
        
    def refresh_timer_label(self):
        self.timer_label.configure(text=self.timer)

    def set_time(self):
        self.timer.time = ConfigManager().load_param("pomodoro_time")
        self.refresh_timer_label()

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
            self.refresh_timer_label()
            if self.timer.is_finished:
                sleep = 1000
                self.bell()
            self.after(sleep, self.pomodoro)


if __name__ == '__main__':
    app = App()
    app.mainloop()