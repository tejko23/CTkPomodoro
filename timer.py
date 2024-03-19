from datetime import datetime, timedelta
    
class TimeCounter:
    def __init__(self, time: str):
        self._time = None
        self.time = time
        self._end_time = datetime.now()
        self.is_running = False
        self.is_finished = False
    
    def __str__(self) -> str:
        return self.time

    @property 
    def time(self) -> str: 
        if self.is_running:
            if datetime.now() < self._end_time:
                self._time = self._end_time - datetime.now()
            else:
                self.is_finished = True
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
        self.is_finished = False
    
    def toggle(self):
        self.is_running = not self.is_running
        if self.is_running:
            self._end_time = datetime.now() + self._time