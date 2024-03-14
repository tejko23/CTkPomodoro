import datetime
import time

import customtkinter

from spinbox import Spinbox
from timer import Timer

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.started = False

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
        
        self.timer = Timer(self.spinbox.get())
        
        self.set_timer_label()
        
    def set_timer_label(self):
        self.timer_label.configure(text=self.timer)

    def set_time(self):
        self.timer.time = self.spinbox.get()
        self.set_timer_label()

    def manage(self):
        if not self.started:
            if self.timer.is_finished():
                self.set_time()
            self.started = True
            self.button.configure(text="Stop")
            self.pomodoro()
        else:
            self.started = False
            self.button.configure(text="Start")

    def pomodoro(self):
        if self.started:
            self.timer.process()
            self.set_timer_label()
            if self.timer.is_finished():
                self.bell()
            self.after(1000, self.pomodoro)


if __name__ == '__main__':
    app = App()
    app.mainloop()