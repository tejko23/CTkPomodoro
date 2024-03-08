import datetime
import time

import customtkinter

from spinbox import Spinbox

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
        
        self.spinbox = Spinbox(self, step_size=5)
        self.spinbox.grid(row=1, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.update_btn = customtkinter.CTkButton(self, 
                                              text="Update", 
                                              command=self.update)
        self.update_btn.grid(row=2, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.button = customtkinter.CTkButton(self, 
                                              text="Start", 
                                              command=self.start)
        self.button.grid(row=3, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        
        self.timer = customtkinter.CTkLabel(self,  
                                            font=customtkinter.CTkFont(
                                                size=50
                                                ))
        self.timer.grid(row=4, 
                          column=0, 
                          padx=20, 
                          pady=20, 
                          sticky="ew", 
                          columnspan=2)
        
        self.set_timer(self.spinbox.get())
        
    def set_timer(self, minutes: str):
        dt_obj = datetime.datetime.strptime(minutes, "%M")
        dt_str = datetime.datetime.strftime(dt_obj, "%M:%S")
        self.timer.configure(text=dt_str)


    def start(self):
        if not self.started:
            if self.timer.cget("text") == "00:00":
                self.update()
            self.started = True
            self.button.configure(text="Stop")
            self.pomodoro()
        else:
            self.started = False
            self.button.configure(text="Start")

    def pomodoro(self):
        if self.started:
            t = datetime.datetime.strptime(self.timer.cget("text"), "%M:%S")
            td = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            if td > datetime.timedelta.resolution:
                t = t - datetime.timedelta(seconds=1)
                self.timer.configure(text=datetime.datetime.strftime(t, "%M:%S"))
            if td == datetime.timedelta(seconds=0):
                self.bell()
            self.timer.after(1000, self.pomodoro)


    def update(self):
        self.set_timer(self.spinbox.get())


        

if __name__ == '__main__':
    app = App()
    app.mainloop()