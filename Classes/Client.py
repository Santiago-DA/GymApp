from datetime import date,datetime
from Classes.Session import Session
from Classes.GenderEnum import Gender
import copy


class Client:
    def __init__(self, name:str, lastName:str, weight:float, height:float, birthDate:datetime,gender:Gender):
        self.name:str = name.capitalize().strip()
        self.lastName:str = lastName.capitalize().strip()
        self.weight:float = weight #should be in kilograms
        self.height:float = height #should be in meters
        self.birthDate:datetime = birthDate #Should be dd/mm/yyyy
        self.sessions:list[Session] = []
        self.gender:Gender = gender #femenino/masculino
    
    @property
    def age(self)->int:
        today = date.today()
        age =  today.year - self.birthDate.year - ((today.month, today.day) < (self.birthDate.month, self.birthDate.day))
        return age
    
    #Body Mass Index
    def CaculateBMI(self)-> float:
        return round(self.weight/self.height**2,2)
    #Basal Metabolic Rato #number is per day
    
    def CalculateBMR(self)->int:
        heightInCM = self.height*100
        if self.gender.name == "MALE":
            sub = 66.4730 + (13.7516*self.weight)+(5.0033*heightInCM)-(6.7550*self.age)
            return round(sub*1.35)
        elif self.gender.name == "FEMALE":
            sub = 655.0955 + (9.5634*self.weight) +(1.8496*heightInCM)-(4.6756*self.age)
            return round(sub*1.35)

    @property
    def fullName(self) ->str:
        return f"{self.name} {self.lastName}"
    
    def __str__(self) -> str:
        return f"Cliente({self.fullName} {self.age}{self.gender.value[0]}, peso:{self.weight}kg, altura:{self.height}m)"
    
    def __repr__(self) -> str:
        return f"Cliente({self.fullName} {self.age}{self.gender.value[0]}, peso:{self.weight}kg, altura:{self.height}m)"

    def __deepcopy__(self, memo):
        # Create a new instance of Client with deep copied attributes
        new_client = Client(
            copy.deepcopy(self.name, memo),
            copy.deepcopy(self.lastName, memo),
            copy.deepcopy(self.weight, memo),
            copy.deepcopy(self.height, memo),
            copy.deepcopy(self.birthDate, memo),
            copy.deepcopy(self.gender, memo)
        )
        new_client.sessions = copy.deepcopy(self.sessions, memo)
        return new_client
