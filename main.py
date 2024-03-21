import app
import event_handlers

if __name__ == '__main__':
    pomodoro_app = app.App()
    event_handlers = event_handlers.PomodoroEventHandler(pomodoro_app)
    pomodoro_app.mainloop()