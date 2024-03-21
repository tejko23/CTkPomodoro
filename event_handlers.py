from app import App
from settings import ConfigManager
from timer import Timer, TimerState, Observer


class PomodoroEventHandler(Observer):
    def __init__(self, app: App):
        self.app: App = app
        self.timer = Timer(ConfigManager().load_param("pomodoro_time"), 
                           self.update)
        self._init_buttons_and_clock_commands()

    def update(self, state: TimerState) -> None:
        self.state = state
        if self.state == TimerState.RUNNING:
            self._set_to_running_cfg()
        elif self.state == TimerState.STOPPED:
            self._set_to_stopped_cfg()
        elif self.state == TimerState.FINISHED:
            self._set_to_finished_cfg()

    def stop(self) -> None:
        self.timer.toggle()

    def start(self) -> None:
        self.timer.toggle()
        self.pomodoro()

    def set_time(self) -> None:
        self.timer.time = ConfigManager().load_param("pomodoro_time")
        self.app.clock.time = self.timer

    def alert(self) -> None:
        if self.state == TimerState.FINISHED:
            self.app.bell()
            self._job = self.app.after(2000, self.alert)
        else:
            self.app.after_cancel(self._job)

    def pomodoro(self) -> None:
        if self.state == TimerState.RUNNING:
            self.app.clock.time = self.timer
            self._job = self.app.after(200, self.pomodoro)
        else:
            self.app.after_cancel(self._job)

    def _init_buttons_and_clock_commands(self) -> None:
        self.app.button.configure(command=self.start)
        self.app.update_btn.configure(command=self.set_time)
        self.app.clock.time = self.timer

    def _set_to_running_cfg(self) -> None:
        self.app.button.configure(text="Stop")
        self.app.button.configure(command=self.stop)

    def _set_to_stopped_cfg(self) -> None:
        self.app.button.configure(text="Start")
        self.app.button.configure(command=self.start)

    def _set_to_finished_cfg(self) -> None:
        self.app.button.configure(command=self.set_time)
        self.alert()