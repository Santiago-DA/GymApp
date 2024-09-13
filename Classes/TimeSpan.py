from datetime import datetime
import math

class TimeSpan():
    def __init__(self, hours: str = "", minutes: str = "", totalTime: int = 0) -> None:
        self.hours:str = hours
        self.minutes:str = minutes
        self.totalTime:int = totalTime
    
    def calculateTime(self, start:datetime, end:datetime)->None:
        
        #format 
        start = datetime.strptime(start, "%H:%M")
        end = datetime.strptime(end, "%H:%M")
        
        difference = end-start
        self.hours = math.floor(difference.seconds/3600)
        
        self.minutes = (difference.seconds // 60) % 60
        self.calculateTotalTimeInMinutes()
    
    def calculateTotalTimeInMinutes(self):
        self.totalTime = int(self.hours) * 60 + int(self.minutes)

    def __str__(self) -> str:
        return f"{self.hours} horas y {self.minutes} minutos"

    def getFormatedTime(self)->str:
        return f"{self.hours:02}:{self.minutes:02}"
    
    def __deepcopy__(self, memo):
        # Create a new instance of TimeSpan with the same values
        return TimeSpan(
            self.hours,
            self.minutes,
            self.totalTime
        )
