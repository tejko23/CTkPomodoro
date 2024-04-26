from .timer import Timer, StateController
from .settings import ConfigManager


class Model:
    def __init__(self) -> None:
        self.config = ConfigManager()
        self.state = StateController()
        self.sequence = PomodoroSequence(
            interval=int(self.config.get_long_break_interval())
        )
        self._settings_time: str = getattr(
            self.config, f"get_{next(self.sequence)}_time"
        )()
        self.timer = Timer(self._settings_time)

    def start_timer(self):
        self.state.start()
        self.timer.set_end_time_to_correct()

    def stop_timer(self):
        if self.state.is_finished():
            self.reset_timer()
        self.state.stop()

    def reset_timer(self):
        time: str = getattr(self.config, f"get_{next(self.sequence)}_time")()
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
        self.sequence.set_current(time_type)


class PomodoroSequence:
    def __init__(self, interval: int = 4) -> None:
        self.interval = interval
        self.phases = self._create_cycle()
        self._next = 0
        self.current = self.phases[self._next]

    def __next__(self) -> str:
        self.current = self.phases[self._next]
        self._next = (self._next + 1) % len(self.phases)
        return self.current

    def set_current(self, value: str) -> None:
        """
        Sets the current phase to the given value.
        :param value: The phase to set as the current phase. It should be
        one of: "pomodoro", "break", or "long_break".
        """
        try:
            self._next = self.phases.index(value)
            self.current = self.phases[self._next]
        except ValueError:
            print(f"{value} is not a valid phase in the cycle.")
        self._next = (self._next + 1) % len(self.phases)

    def get_current_type(self) -> str:
        return self.current

    def set_interval(self, value: int) -> None:
        self.interval = value
        self.phases = self._create_cycle()
        self.set_current(self.current)

    def _create_cycle(self):
        cycle = ["pomodoro", "break"] * (self.interval - 1)
        cycle.extend(["pomodoro", "long_break"])
        return cycle
