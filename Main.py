from internet import MakerConnection
from defspins import PinReset
import web
import grafico#funcao em c++
import uasyncio as asyncro
#nao sei como tá a identificação já que nao tem tab disponível
#Classe de intermédio entre o front e o back, tem que ser equeno, vai so chamar as coisas
class Main:

    PORT = 80
    IP = "0.0.0.0"
   
    def __init__(self, internetName:str=None, password=None)->None:
        self.internetName = internetName
        self.password = password
        self.serverToken = MakerConnection(self.internetName, self.password)
        self.reset = PinReset()


        self.task_grafic = None
        self.task_sound = None
        self.task_resetPin = None
        self.task_checkInternt = None
       
    def check_task(self, task, exe):
        if task is None:
           return asyncro.create_task(exe())
           
        return task
   
    async def begin_server(self):
        await uasyncio.start_server(self.request_route, self.IP, self.PORT)
    
    async def resquests_route(self, reader, writer):
       
        while True:
            self.task_resetPin = self.check_task(self.task_resetPin, self.check_resetPin)
            self.task_checkInternet = self.check_task(self.task_checkInternet, elf.checkInternet)
           
            linha = await reader.readline()
            requestPage = line.decode().split(" ")[1]
           
            if requestPage == "/":
                selfLog = self.self_login()
                if not selfLog:
              #setar menssagem falando q nao deu pra se conectar
                else:
                    renderTemplates.configPage()
                    continue                   

            elif requestPage.startwith("/config"):
                typeDataValue = requestPage.split("?")[1]
                self.task_grafic = self.check_task(self.task_grafic, self.checkGrafic)
                self.task_sound = self.check_task(self.task_sound, self.checkSound)
                if "=" in requestPage:
                    dataValue = requestPage.split("=")[1]
            
    def run_app(self)->dict:
        self.serverConnection = self.serverToken.begin_connection()
        self.connectedIn = self.serverToken.socket_accept()...
        clientServer = {"Id": self.internetName,
                       "Servidor": self.connectedIn[0]}
        
        return clientServer
       
       
    def wifis_around(self)->list[dict]:
        wifisAround = self.serverToken.wifis_scans()
        wifis = [{"Rede": _wifi_[0].decode(), "Potência do sinal": _wifi_[3]} for _wifi_ in wifisAround]
        return wifis

   
    def config_selfconnection(self, setSelfConn:bool=False)->None:
        self.serverToken.is_selfconnection(setSelfConn)
        
    
    def self_login(self)->dict | bool:        
        datasToSelfConn = self.serverToken.make_selfconnection()
        if datasToSelfConn:
            self.internetName, self.password = datasToSelfConn[0], datasToSelfConn[1]
            self.serverToken = MakerConnection(self.internetName, self.password)
            self.run_app()
            return True

        return False
       
       
if __name__ == "__main__":
    try:
        runner = Main()   
    except:
        print('Deu merda')


