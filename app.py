import customtkinter

from spinbox import Spinbox

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro")
        self.geometry("400x200")
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
        

if __name__ == '__main__':
    app = App()
    app.mainloop()