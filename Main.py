from internet import MakerConnection
from defspins import PinReset
import web
import grafico#funcao em c++
import uasyncio as asyncro
#nao sei como tá a identificação já que nao tem tab disponível
#Classe de intermédio entre o front e o back, tem que ser equeno, vai so chamar as coisas
class Main:
   
    def __init__(self, internetName:str=None, password=None)->None:
        self.internetName = internetName
        self.password = password
        self.serverToken = MakerConnection(self.internetName, self.password)
        self.serverSocket = self.serverToken.begin_socket()
        self.reset = PinReset()
       
    async def gerated_asycro_defs(self, pagesOn):
       while True:
           task_reset = asyncro.create_task(self.reset.check_reset())
       
           if pageOn["page"] == "config":
               task_grafic = asyncro.create_task(self.grafic())
           if pageResquest == "vol":  
               task_sound = asyncro.create_task(self.sound_collector())
       
    def run_app(self)->dict:
        self.serverConnection = self.serverToken.begin_connection()
        self.connectedIn = self.serverToken.socket_accept()
        clientServer = {"Id": self.internetName,
                       "Servidor": self.connectedIn[0]}
        return clientServer
       
       
    def wifis_around(self)->list[dict]:
        wifisAround = self.serverToken.wifis_scans()
        wifis = [{"Rede": _wifi_[0].decode(), "Potência do sinal": _wifi_[3]} for _wifi_ in wifisAround]
        return wifis

   
    def config_autoconnection(self, setSelfConn:bool=False)->None:
        self.serverToken.is_selfconnection(setSelfConn)
        
    
    def auto_login(self)->dict | bool:        
        datasToSelfConn= self.serverToken.make_selfconnection()
        if datasToSelfConn:
            self.internetName, self.password = datasToSelfConn[0], datasToSelfConn[1]
            self.serverToken = MakerConnection(self.internetName, self.password)
            response = self.asyncro_bus()
            return response

        return False
       
       
if __name__ == "__main__":
    try:
        runner = Main()   
    except:
        print('Deu merda')


