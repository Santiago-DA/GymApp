from typing import List, Tuple
from Classes.GenderEnum import Gender
from Classes.Client import Client
from Classes.Session import Session
from Classes.FormatManager import FormatManager
from Classes.METEnum import METs
from FileManagement.FileManager import FileManager


from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivymd.uix.list import MDList
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.button import MDRaisedButton
import time

def getActiveSession(clients:List[Client]):
    activeSessions:List[Tuple[Session,str]] = []
    for client in clients:
        for session in client.sessions:
            if session.ended == False:
                activeSessions.append((session,client.fullName))
    return activeSessions

#*GLOBAL VARIABLES
Clients:list[Client] = FileManager.loadInfo()
ActiveSessions = getActiveSession(Clients)
class ClientListItem(ThreeLineListItem):
    def __init__(self, client: Client, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client = client

class SessionListItem(ThreeLineListItem):
    def __init__(self, session: Session, **kwargs) -> None:
        super().__init__(**kwargs)
        self.session = session

class SessionModalButton(MDRaisedButton):
    def __init__(self, session: Session, **kwargs) -> None:
        super().__init__(**kwargs)
        self.session = session

class IndiosGymApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        kv = Builder.load_file("t.kv")
        return kv

    #+ Navigation Functions
    def change_screen(self,screen_name:str):
        if (screen_name == "CreateClient"):
            self.clearCreateClientScreen()
        elif (screen_name == "CreateSession"):
            self.clearCreateSessionScreen()
        elif (screen_name == "Clientes"):
            self.populateClientList()
        elif (screen_name == "Sesiones"):
            self.populateSessions()
        self.root.ids.screen_manager.current = screen_name
    
    def clearCreateClientScreen(self):
        self.root.ids.name_field.text = "" 
        self.root.ids.last_name_field.text = ""
        self.root.ids.weight_field.text = ""
        self.root.ids.height_field.text = ""
        self.root.ids.gender_field.text = ""
        self.root.ids.gender_field.error = False
        self.root.ids.date_field.text = ""
    
    def createClient(self):
        #*1.get the textsFields text
        name = self.root.ids.name_field.text
        lastName = self.root.ids.last_name_field.text
        height = self.root.ids.height_field.text
        weight = self.root.ids.weight_field.text
        gender = self.root.ids.gender_field.text
        birthDate = self.root.ids.date_field.text
        
        #*2.check if any of them are ""
        emptys:list[bool] = []
        emptys.append(FormatManager.isEmptyText(name))
        emptys.append(FormatManager.isEmptyText(lastName))
        emptys.append(FormatManager.isEmptyText(height))
        emptys.append(FormatManager.isEmptyText(weight))
        emptys.append(FormatManager.isEmptyText(gender))
        emptys.append(FormatManager.isEmptyText(birthDate))

        if any(emptys):
            MDSnackbar(
                MDLabel(text="Todos los campos deben de estar llenos")
            ).open()
            return
        
        if (not FormatManager.checkValidGender(gender)):
            MDSnackbar(
                MDLabel(text="Genero no valido")
            ).open()
            return
        
        if not FormatManager.isValidDate(birthDate):
            MDSnackbar(
                MDLabel(text="Fecha no valida")
            ).open()
            return

        #*3 Format 
        name = FormatManager.formatName(name)
        lastName = FormatManager.formatName(lastName)
        height = FormatManager.toFloat(height)
        weight = FormatManager.toFloat(weight)
        birthDate = FormatManager.convertStringToDate(birthDate)
        gender = Gender.MALE if gender =="masculino" else Gender.FEMALE
        #*Save it
        newClient = Client(name,lastName,weight,height,birthDate,gender)
        print(newClient)
        Clients.append(newClient)
        Clients.sort(key=lambda client:client.fullName)
        FileManager.saveInfo(Clients)
        self.change_screen("Clientes")
        MDSnackbar(
            MDLabel(text=f"Cliente: {newClient.fullName} creado con exito")
        ).open()
    
    def validateGender(self,instance:MDTextField,text):
        if text not in [item.value for item in Gender]:
            instance.error = True
        else:
            instance.error = False
    
    def clearCreateSessionScreen(self):#TODO
        self.root.ids.select_clients.text = "Selecionar cliente"
        self.root.ids.select_intensity.text = "Selecionar Intensidad"
    
    def openClientSelection(self):
        def changeSelectClientText(str):
            self.root.ids.select_clients.text = str
        if len(Clients) == 0:
            MDDropdownMenu(caller=self.root.ids.select_clients, items=[]).open()
            return
        
        menuItems = [
            {
                "text" : client.fullName,
                "on_release" : lambda x=client.fullName:changeSelectClientText(x)
            }
            for client in Clients
        ]
        MDDropdownMenu(caller=self.root.ids.select_clients, items=menuItems).open()
    
    def openIntensitySelection(self):
        def changeSelectintensityText(str):
            self.root.ids.select_intensity.text = str
        menuItems = [
            {
                "text" : intensity.value[1],
                "on_release" : lambda x=intensity.value[1]:changeSelectintensityText(x)
            }for intensity in METs
        ]
        MDDropdownMenu(caller=self.root.ids.select_intensity, items=menuItems).open()

    def createSession(self):
        clientName = self.root.ids.select_clients.text
        intensity = self.root.ids.select_intensity.text
        if clientName == "Selecionar cliente" :
            MDSnackbar(
                MDLabel(text="Debe de selecionar un cliente")
            ).open()
            return
        elif intensity == "Selecionar Intensidad":
            MDSnackbar(
                MDLabel(text="Debe de selecionar una intensidad")
            ).open()
            return
        
        met = self.searchMETbyName(intensity)
        client = self.searchClientByName(clientName)
        #2.create session 
        session = Session(met)
        #3.append it to client
        client.sessions.append(session)
        #4.Save it to file
        ActiveSessions.append((session,client.fullName))
        FileManager.saveInfo(Clients)
        
        #5.Snackbar
        self.change_screen("Sesiones")
        auxText = f"Sesión de {client.fullName} {session.date}-{session.startTime} creada con exito"
        MDSnackbar(MDLabel(text=auxText)).open()
        
    def searchMETbyName(self,intensity:str):
        for met in METs:
            if met.value[1] == intensity:
                return met
        return METs.EJERCISIO_LIGERO
    
    def searchClientByName(self,name:str):
        if len(Clients) == 0:
            return
        for client in Clients:
            if name == client.fullName:
                return client
        return None
    
    def fillClientProfile(self,client:Client):
        def loadSessionClientProfile(client:Client):
            if len(client.sessions) == 0:
                return
            sessionList:MDList = self.root.ids.profileSessionList
            sessionList.clear_widgets()
            for session in reversed(client.sessions):
                if session.ended == True:
                    sessionItem = SessionListItem(session=session)
                    sessionItem.text = session.intensity.value[1]
                    sessionItem.secondary_text = f"Calorias aproximadas: {session.CalculateCaloriesBurned(client.weight)}"
                    sessionItem.tertiary_text = f"{session.date} - {session.timeSpan.getFormatedTime()}"
                    
                    sessionList.add_widget(sessionItem)
        def loadPersonalData(client:Client):
            self.root.ids.genderAgeData.text = f"{client.gender.value} - edad: {client.age}"
            self.root.ids.bdiData.text = f"BMI: {client.CaculateBMI()}"
            self.root.ids.heightWeightData.text = f"{client.height}m - {client.weight}kg"
            self.root.ids.bmrData.text = f"consumo calorico diario: {client.CalculateBMR()}cal"
        
        
        self.root.ids.tittleName.title = client.fullName
        loadPersonalData(client)
        loadSessionClientProfile(client)
        self.change_screen("Client Profile")
    
    def populateClientList(self):
        if len(Clients) == 0:
            return
        clientList:MDList = self.root.ids.clients_list
        clientList.clear_widgets()
        for index, client in enumerate(Clients):
            itemList = ClientListItem(
                client = client,
                text = client.fullName,
                on_release=lambda x, client=client: self.fillClientProfile(client)
            )
            clientList.add_widget(itemList)
    
    def populateSessions(self):
        ActiveSessions = getActiveSession(Clients)
        if len(ActiveSessions) == 0:
            return
        SessionList:MDList = self.root.ids.session_list
        SessionList.clear_widgets()
        for session, owner in ActiveSessions:
            newSessionItem = SessionListItem(session=session)
            newSessionItem.text = owner
            newSessionItem.secondary_text = session.intensity.value[1]
            newSessionItem.tertiary_text = session.date
            
            newSessionItem.bind(on_release=self.openSessionItemModal)
            SessionList.add_widget(newSessionItem)
    
    def openSessionItemModal(self,instance:SessionListItem):#TODO
        def endSession(session:Session,dialog:MDDialog,owner:str):
            session.setEndTime()
            dialog.dismiss()
            ActiveSessions.remove((session,owner))
            MDSnackbar(
                MDLabel(text=f"Sesión de {session.timeSpan.getFormatedTime()} tiempo terminada con exito")
            ).open()
            FileManager.saveInfo(Clients)
            self.change_screen("Clientes")
            time.sleep(0.3)
            self.change_screen("Sesiones")
            self.root.ids.session_list.clear_widgets()
        
        session = instance.session
        name = ""
        for client in Clients:
            if session in client.sessions:
                name = client.fullName
        dialog = MDDialog(
            title=name,  # Use title for the dialog headline
            type="custom",  # Use "custom" to create a custom dialog layout
            items=[
                MDLabel(text=f"{session.startTime}/--:--")
            ],
            buttons=[
                MDRaisedButton(
                    text="Finalizar",
                    on_release=lambda btn: endSession(session, dialog, name)
                )
            ]
        )
        
        dialog.open()

    def on_start(self):
        self.loadHomeScreen()
    
    def loadHomeScreen(self):
        clientNumber = len(Clients)
        activeSessionNumber = len(ActiveSessions)
        self.root.ids.homeLabel.text = f"Bienvenido\nClientes: {clientNumber} / Sesiones Activas: {activeSessionNumber}"


def main():
    IndiosGymApp().run()

if __name__ == "__main__":
    main()