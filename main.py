from pomodoro import Model, Pomodoro, PomodoroPresenter


def main() -> None:
    model = Model()
    view = Pomodoro()
    presenter = PomodoroPresenter(view, model)
    presenter.run()


if __name__ == "__main__":
    main()
