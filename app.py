import datetime
import time

import customtkinter

from spinbox import Spinbox
from timer import TimeCounter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro")
        self.geometry("400x400")
        self.grid_columnconfigure((0, 1), weight=1)

        self.label = customtkinter.CTkLabel(self, text="Pomodoro", 
                                            font=customtkinter.CTkFont(
                                                size=50
                                                ))
        self.label.grid(row=0, 
                        column=0, 
                        padx=20, 
                        pady=20, 
                        sticky='ew', 
                        columnspan=2)
        
        self.spinbox = Spinbox(self, entry="5", step_size=1)
        self.spinbox.grid(row=1, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.update_btn = customtkinter.CTkButton(self, 
                                              text="Set time", 
                                              command=self.set_time)
        self.update_btn.grid(row=2, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
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
        
        
        self.timer_label = customtkinter.CTkLabel(self,  
                                            font=customtkinter.CTkFont(
                                                size=50
                                                ))
        self.timer_label.grid(row=4, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.timer = TimeCounter(self.spinbox.get())
        
        self.refresh_timer_label()
        
    def refresh_timer_label(self):
        self.timer_label.configure(text=self.timer)

    def set_time(self):
        self.timer.time = self.spinbox.get()
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