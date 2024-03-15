from datetime import datetime, timedelta

class Timer:
    def __init__(self, time: str):
        self._time = None
        self.time = time 

    def __str__(self) -> str:
        return self.time

    @property 
    def time(self) -> str: 
        mm, ss = divmod(self._time.seconds, 60)
        return f"{mm:02}:{ss:02}"

    @time.setter 
    def time(self, time_value: str) -> None: 
        if not isinstance(time_value, str):
            raise ValueError(f"{time_value} must be str.") 
        self._time = timedelta(minutes=int(time_value))
        
    def process(self):
        if self._time > timedelta.resolution:
            self._time -= timedelta(seconds=1)

    def is_finished(self) -> bool:
        if self._time == timedelta(seconds=0):
            return True
        return False