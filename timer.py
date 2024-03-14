from datetime import datetime, timedelta

class Timer:
    def __init__(self, time: str):
        self._time = None
        self._delta = None
        self.time = time 

    def __str__(self) -> str:
        return self.time

    @property 
    def time(self) -> str: 
        return datetime.strftime(self._time, "%M:%S")

    @time.setter 
    def time(self, time_value: str) -> None: 
        if not isinstance(time_value, str):
            raise ValueError(f"{time_value} must be str.") 
        self._time = datetime.strptime(time_value, "%M")
        self._update_delta()
        
    def _update_delta(self) -> None:
        self._delta = timedelta(hours=self._time.hour,
                                minutes=self._time.minute,
                                seconds=self._time.second)
        
    def process(self):
        if self._delta > timedelta.resolution:
            self._time -= timedelta(seconds=1)
            self._update_delta()

    def is_finished(self) -> bool:
        if self._delta == timedelta(seconds=0):
            return True
        return False