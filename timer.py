from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum

class TimerState(Enum):
    RUNNING = 'running'
    STOPPED = 'stopped'
    FINISHED = 'finished'

class Observer(ABC):
    @abstractmethod
    def update(self, state: TimerState):
        pass
    
class Timer:
    def __init__(self, time: str, fn):
        self._post_state = fn
        self._time = None
        self.time = time
        self._end_time = datetime.now()
        self.state = TimerState.STOPPED
    
    def __str__(self) -> str:
        return self.time

    @property 
    def time(self) -> str: 
        if self.state == TimerState.RUNNING:
            if datetime.now() < self._end_time:
                self._time = self._end_time - datetime.now()
            else:
                self.set_state(TimerState.FINISHED)
        mm, ss = divmod(self._time.seconds, 60)
        return f"{mm:02}:{ss:02}"

    @time.setter
    def time(self, time_value: str):
        if not isinstance(time_value, str):
            raise TypeError(f"Input {time_value} must be a string.")
        
        try:
            if ':' in time_value:
                minutes, seconds = map(int, time_value.split(':'))
                self._time = timedelta(minutes=minutes,
                                       seconds=seconds)
            else:
                self._time = timedelta(minutes=int(time_value))
        except ValueError:
            raise ValueError(
                "Invalid time format. Please provide time in the format \
                    'MM:SS' or 'M'."
                )
        self.set_state(TimerState.STOPPED)

    def set_state(self, state: TimerState):
        self.state = state
        self._post_state(self.state)
    
    def toggle(self):
        if self.state == TimerState.STOPPED:
            self.set_state(TimerState.RUNNING)
            self._end_time = datetime.now() + self._time
        elif (self.state == TimerState.RUNNING 
              or self.state == TimerState.FINISHED):
            self.set_state(TimerState.STOPPED)
