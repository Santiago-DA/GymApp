
from datetime import datetime as dt
class FormatManager():
    #from "yyyy-mm-dd" to "dd/mm/yyyy"
    def formatDate(date_str):
        date = dt.strptime(date_str,"%Y-%m-%d")
        return date.strftime("%d/%m/%Y")
    
    def formatName(name:str) ->str:
        return name.strip().capitalize()
    
    def toFloat(quantity:str):
        try:
            return float(quantity)
        except:
            raise ValueError("Error: value given is not float convertable")
    
    def convertStringToDate(date_str):
        aux = dt.strptime(date_str,"%d/%m/%Y")
        return aux

    def isValidDate(date_str) ->bool:
        if not date_str:
            return False
        try:
            dt.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def isEmptyText(text:str)->bool:
        return True if text == "" else False
    
    def checkValidGender(text:str)->bool:
        return True if text in ["femenino","masculino"] else False