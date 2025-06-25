import network as net
from definicao_dos_pinos import Sockets
import ujson
from erros import ErroWLAN
from time import sleep



class Internet:  


    #eu nao quero fazer hierarquia entre internet e cofigWifi já que configWifi é uma classe muito aberta
    #preferi reiniciar o construtor pra manter a independencia entre as duas classes
    def __init__(self, nameNetwork, keyNetwork)->None:
        self._nameNetwork = nameNetwork
        self._keyNetwork = keyNetwork
        self.wifi = None


       
    def create_network(self)->bool:
        try:
            self.wifi = net.WLAN(net.STA_IF)
            self.wifi.active(True)
            return True
            
        except  Exception:
            fatal_error = ErroWLAN()
            return fatal_error.pin_error()
    
    
    def verif_conn(self)->None:
       
       if not self.wifi.isconnected():
           self.wifi.connect(self._nameNetwork, self._keyNetwork)
             
       
    def conect_network(self)->bool:
        if self.create_network():
                self.verif_conn()
                
                for _ in range(10):
                    
                    if self.wifi.isconnected():
                        return True
                        
                    sleep(1)                    
                
        return False


    def network_scans(self)->list[tuple]:
        wifis_scans = self.wifi.scan()
        return wifis_scans




class ConfigWifi:
   
    def __init__(self, wifiName, password)->None:
        self._wifiName = wifiName
        self._password = password
       
       
    @property
    def wifi_name(self)->str:
        return self._wifiName
       
       
    @property
    def wifi_password(self)->str:
        return self._password
       
       
    @property
    def data_wifi(self)->dict[str, str] :
        return {"wifi": self.wifi_name, "password": self.wifi_password}
       
       
    def save_wifi_info(self)->None:      
        with open('wifi_login.json', 'w') as j:          
            ujson.dump(self.data_wifi, j)
           
           
    def change_wifi_info(self)->tuple[str, str] | tuple[None, None]:        
        try:
            with open('wifi_login.json', 'r') as j:          
                data = ujson.load(j)
                return data["wifi"], data["password"]
               
        except:
            return None, None  

    def make_autoreconnection(self, response)->None:
        with open('autologin.json', "w") as j:
            ujson.dump({"autoconexão": response}, j)
        
        
    def return_autoconnection(self)->bool:
        with open('autologin.json', "r") as j:
            isauto = ujson.load(j)
            return isauto["autoconexão"]
        


class MakerConnection:
   
    def __init__(self, internetName:str, password)->None:
        self.internetName = internetName
        self.password = password
        self.w = ConfigWifi(self.internetName, self.password)
       
       
    def begin_socket(self):
       
        self.server = Sockets()
        self.socket_ = self.server.config_socket()
        return self.socket_
   
       
    def get_ssid_and_password_json(self):
        return self.w.change_wifi_info()
        

    def begin_connection(self):          
        self.internetServer = Internet(self.internetName, self.password)
        self.connection = self.internetServer.connect_network()
        
        if self.connection:
            self.w.save_wifi_info()
       
        return self.connection
       
           
    def set_autoconnection(self, autoconn)->None:
        self.make_autoreconnection(autoconn)
        
        
    def is_autoconnection()->bool:
        if self.return_autoconnectio():
        #varrer todos os scans
        #veficiar se existe em existe uma rede salva ,no json de redes salvas, o id do scan
        #se houver, o password salvo no json de redes e o nome da rede serão usados em verif_conn()
        #a senha e id serao passados para verif_conn
        #isso deve acontecer apenas se ainda nao estiver cknectado a outra ou a mesma rede
        #implementar de maneira que nao entre em conflito com begin connection
            
        
        
    def wifis_scans(self):
        return self.internetServer.network_scans()
       
       
    def socket_accept(self):
        return self.server.socket_accept()
        
        