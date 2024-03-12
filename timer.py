from datetime import datetime, timedelta

class Timer:
    def __init__(self, time):
        self.time = self._str_minutes_to_datetime(time)
        
    def _str_minutes_to_datetime(self, minutes: str) -> datetime:
        return datetime.strptime(minutes, "%M")
    
    def process(self):
        delta = timedelta(hours=self.time.hour,
                          minutes=self.time.minute,
                          seconds=self.time.second)
        if delta > timedelta.resolution:
            self.time -= timedelta(seconds=1)
        
    def get_current_str_time(self) -> str:
        return datetime.strftime(self.time, "%M:%S")
    
    def set_time(self, minutes: str):
        self.time = self._str_minutes_to_datetime(minutes)

    def is_finished(self) -> bool:
        delta = timedelta(hours=self.time.hour,
                          minutes=self.time.minute,
                          seconds=self.time.second)
        if delta == timedelta(seconds=0):
            return True
        return False