from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict


class TimerState(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    FINISHED = "finished"


class Borg:
    _shared_state: Dict[str, Any] = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class StateController(Borg):
    def __init__(self):
        super().__init__()
        self.state = TimerState.STOPPED

    def start(self):
        self.state = TimerState.RUNNING

    def stop(self):
        self.state = TimerState.STOPPED

    def finish(self):
        self.state = TimerState.FINISHED

    def is_running(self):
        return self.state is TimerState.RUNNING

    def is_finished(self):
        return self.state is TimerState.FINISHED

    def is_stopped(self):
        return self.state is TimerState.STOPPED


class Timer:
    def __init__(self, time: str):
        self.state = StateController()
        self._time: timedelta = timedelta()
        self.time: str = time
        self._end_time: datetime = datetime.now() + self._time

    def __str__(self) -> str:
        return self.time

    @property
    def time(self) -> str:
        if self.state.is_running():
            self._time = self._calculate_time()
        mm, ss = divmod(self._time.seconds, 60)
        return f"{mm:02}:{ss:02}"

    @time.setter
    def time(self, time_value: str):
        if not isinstance(time_value, str):
            raise TypeError(f"Input {time_value} must be a string.")

        try:
            if ":" in time_value:
                minutes, seconds = map(int, time_value.split(":"))
                self._time = timedelta(minutes=minutes, seconds=seconds)
            else:
                self._time = timedelta(minutes=int(time_value))
        except ValueError:
            raise ValueError(
                "Invalid time format. Please provide time in the format \
                    'MM:SS' or 'M'."
            )

    def set_end_time_to_correct(self) -> None:
        self._end_time = datetime.now() + self._time

    def is_completed(self) -> bool:
        """Checks if the timer has finished."""
        current_time = datetime.now()
        return current_time >= self._end_time

    def _calculate_time(self) -> timedelta:
        current_time = datetime.now()
        if current_time < self._end_time:
            return self._end_time - current_time
        else:
            return timedelta()
