import pickle
from typing import Any,List

class FileManager():
    def saveInfo(objects:List[Any]):
        with open("data.pickle", "wb") as file:
            pickle.dump(objects,file)
        print("Info saved")
    def loadInfo():
        with open("data.pickle", "rb") as file:
            print("info loaded")
            return pickle.load(file)

if __name__ == "__main__":
    FileManager.saveInfo([])