import network as net
import ujson
from erros import ErroWLAN
from time import sleep
from definicao_dos_pinos import Sockets


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
       
       
    def data_wifi(self)->dict[str, str]:
        return {"wifi": self.wifi_name, "password": self.wifi_password}

    
    def read_json_wifis(self, file):
        try:
            with open(file, "r") as j:
                json_read = ujson.load(j)      
        except Exception:
            pass

    
    def whrite_json_wifis(self, file, data):    
        if file["wifi"] != None and file["password"] != None:
            with open('wifi_login.json', 'w') as j:
                ujson.dump([data], j)
           
    
    def save_wifi_info(self)->None:
        jsonOppen = self.all_wifis()
        if jsonOppen is None:
            self.whrite_json_wifis(self.data_wifi)
            return
        
        for savedWifi in jsonOppen:
            if savedWifi["wifi"] != self.wifi_name:
                jsonOppen.append(self.data_wifi)
                self.whrite_json_wifis(jsonOppen)

    
    def all_wifis(self)->list[dict()] | None:
        wifi_list = self.read_json_wifis('wifis_saves.json')
        return wifi_list

    
    def set_autoreconnection(self, response)->None:
        with open('autologin.json', "w") as 
            ujson.dump({"autoconexão": response}, j)
        
        
    def return_autoconnection(self)->bool:
        with open('autologin.json', "r") as j:
            isauto = ujson.load(j)
            return isauto["autoconexão"]
        


class MakerConnection:
   
    def __init__(self, internetName:str, password)->None:
        self.internetName = internetName
        #nao acho que crip é necessário 
        self.password = password
        self.w = ConfigWifi(self.internetName, self.password)
       
       
    def begin_socket(self):       
        self.server = Sockets()
        self.socket_ = self.server.config_socket()
        return self.socket_
   
       
    def get_ssid_and_password_json(self):
        return self.w.data_wifi()
        

    def begin_connection(self):          
        self.internetServer = Internet(self.internetName, self.password)
        self.connection = self.internetServer.connect_network()
        
        if self.connection:
            self.w.save_wifi_info()
       
        return self.connection
       
           
    def define_autoconnection(self, autoconn)->None:
        self.w.make_autoreconnection(autoconn)
        
        
    def make_autoconnection()->list[str, str] | bool:
        if self.w.return_autoconnectio():
            get_wifis_saves = self.all_wifis()
            available_wifis = self.wifis_scans()
            for wifi in available_wifis:
                if wifi[0] == self.get_ssid_and_password_json()[0]:
                    return wifi[0], wifi[1]
                    
        return False
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
        
        
