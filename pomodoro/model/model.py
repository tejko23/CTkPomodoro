from .timer import Timer, TimerState, StateController
from .settings import ConfigManager


class Model:
    def __init__(self) -> None:
        self.config = ConfigManager()
        self.state = StateController()
        time: str = self.config.get_pomodoro_time()
        self.timer = Timer(time)

    def stop_timer(self):
        self.state.stop()

    def start_timer(self):
        self.state.start()
        self.timer.refresh_end_time()

    def reset_timer(self):
        time: str = self.config.get_pomodoro_time()
        self.timer.time = time

    def finish_timer_if_done(self):
        if str(self.timer) == "00:00":
            self.state.finish()
