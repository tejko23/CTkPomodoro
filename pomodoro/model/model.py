from .timer import Timer, TimerState, StateController
from .settings import ConfigManager


class Model:
    def __init__(self) -> None:
        self.config = ConfigManager()
        self.state = StateController()
        self._settings_time: str = self.config.get_pomodoro_time()
        self.timer = Timer(self._settings_time)

    def start_timer(self):
        self.state.start()
        self.timer.set_end_time_to_correct()

    def stop_timer(self):
        if self.state.is_finished():
            self.reset_timer()
        self.state.stop()

    def reset_timer(self):
        time: str = self.config.get_pomodoro_time()
        self.timer.time = time

    def finish_timer_if_done(self):
        if self.timer.is_completed():
            self.state.finish()

    def set_time(self, time_type: str):
        valid_types = ("pomodoro", "break", "long_break")
        if time_type not in valid_types:
            raise ValueError(
                f"Invalid time_type: {time_type}. Valid types are: {', '.join(valid_types)}"
            )
        time: str = getattr(self.config, f"get_{time_type}_time")()
        self.timer.time = time
