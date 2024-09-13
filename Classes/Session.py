from datetime import date, datetime
from Classes.TimeSpan import TimeSpan
from Classes.METEnum import METs
from Classes.FormatManager import FormatManager
import copy

class Session():
    def __init__(self, intensity:METs) -> None:
        self.ended = False
        self.date:date = date.today()
        self.date = FormatManager.formatDate(str(self.date))#Formated to dd/mm/YYYY
        self.startTime:datetime = datetime.now()
        self.startTime = self.startTime.strftime("%H:%M")
        self.endTime:datetime = None
        self.timeSpan:TimeSpan = TimeSpan()
        self.intensity:METs = intensity
        
    def setEndTime(self)->None:
        self.endTime = datetime.now()
        self.endTime = self.endTime.strftime("%H:%M")
        self.ended = True
        self.setTotalTime()
    
    def setTotalTime(self)->None:
        aux = TimeSpan()
        aux.calculateTime(self.startTime,self.endTime)
        self.timeSpan = aux
    
    def CalculateCaloriesBurned(self, weight:float) ->int:
        if self.ended:
            return round(int(self.timeSpan.totalTime) * (self.intensity.value[0] * 0.0175 * weight))
        else:
            return -1

    def __str__(self) -> str:
        return f"Session(date:{self.date}, intensity:{self.intensity.value[1]})"
    
    def __deepcopy__(self, memo):
        # Create a new instance of Session with deep copied attributes
        return Session(
            copy.deepcopy(self.intensity, memo)
        ).copy_attributes_from(self)
    
    def copy_attributes_from(self, other):
        self.ended = other.ended
        self.date = other.date
        self.startTime = other.startTime
        self.endTime = other.endTime
        self.timeSpan = copy.deepcopy(other.timeSpan)
