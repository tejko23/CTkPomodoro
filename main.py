from pomodoro import App, PomodoroEventHandler


def main() -> None:
    pomodoro_app = App()
    event_handlers = PomodoroEventHandler(pomodoro_app)
    pomodoro_app.mainloop()


if __name__ == "__main__":
    main()
