import network as net
import ujson
from erros import ErroWLAN, ConnectionError
from time import sleep
from definicao_dos_pinos import Sockets

#Esse arquivo tá finalizado eu não vou mexer nisso de novo por nada nesse mundo
class SettingsInternet:  
    
    def __init__(self, nameNetwork=None, keyNetwork=None)->None:
        self._nameNetwork = nameNetwork
        self._keyNetwork = keyNetwork
        self.wifi = None

       
    def activate_network(self)->bool:
        try:
            self.wifi = net.WLAN(net.STA_IF)
            self.wifi.active(True)
            return True
            
        except Exception:
            fatal_error = ErroWLAN()
            return fatal_error.pin_error()
    
    
    def verif_conn(self)->None:       
       if not self.wifi.isconnected():
           self.wifi.connect(self._nameNetwork, self._keyNetwork)
             
       
    def connect_network(self)->bool:
        if self.activate_network():
            self.verif_conn()
            try:
                for _ in range(10):
                    if self.wifi.isconnected():
                        return True    
                    sleep(1)
                raise ConnectionError()
                
            except ConnectionError as e:
                connect_net_error = e.password_error()
                return connect_net_error


    def network_scans_around(self)->list[tuple]:
        wifis_scans = self.wifi.scan()
        return wifis_scans



class ManagerWifiInfor:
   
    def __init__(self, wifiName, password)->None:
        self._wifiName = wifiName
        self._password = password

    
    def data_wifi(self)->dict[str, str]:
        return {"wifi": self._wifi_name, "password": self._wifi_password}

    
    def read_json_wifis(self, file):
        try:
            with open(file, "r") as j:
                return ujson.load(j)
        
        except (OSError, ValueError):
            print(f"Erro ao ler o arquivo: {file}")
            return None
    
    
    def whrite_json_wifis(self, file, data)->None:
        with open(file, 'w') as j:
            ujson.dump(data, j)
                
    
    def save_wifi_info(self) -> None:
        jsonOppen = self.all_wifis()
        if jsonOppen is None:
            self.whrite_json_wifis("list_wifis.json", [self.data_wifi()])
            return

        for savedWifi in jsonOppen:
            if savedWifi["wifi"] == self._wifi_name:
                return

        jsonOppen.append(self.data_wifi())
        self.whrite_json_wifis("list_wifis.json", jsonOppen)
        
    
    def all_wifis(self)->list[dict()] | None:
        wifi_list = self.read_json_wifis('list_wifis.json')
        return wifi_list

    
    def set_selfconnection(self, response)->None:
        with open('autologin.json', "w") as j:
            ujson.dump({"autoconexão": response}, j)
        
        
    def return_selfconnection(self)->bool:
        with open('autologin.json', "r") as j:
            isauto = ujson.load(j)
            return isauto["autoconexão"]
        


class MakerConnection:
   
    def __init__(self, internetName:str, password)->None:
        self.internetName = internetName
        #nao acho que crip é necessário 
        self.password = password
        self.w = ManagerWifiInfor(self.internetName, self.password)
       
       
    def begin_socket(self):       
        self.server = Sockets()
        self.socket_ = self.server.config_socket()
        return self.socket_
        

    def begin_connection(self)->bool:          
        self.internetServer = SettingsInternet(self.internetName, self.password)
        self.connection = self.internetServer.connect_network()
        
        if self.connection:
            self.w.save_wifi_info()
       
        return self.connection
       
           
    def define_selfconnection(self, autoconn)->None:
        self.w.set_selfconnection(autoconn)
        
        
    def make_selfconnection(self)->tuple[str, str] | bool:
            
        autocon = self.w.return_selfconnection()
        if autocon:
            get_wifis_saves = self.w.all_wifis()
            available_wifis = self.wifis_scans()
            
            if get_wifis_saves is None or not get_wifis_saves or not available_wifis:
                print("Nenhuma rede salva para tentar conexão automática.")
                return False
            
            for wifi in available_wifis:
                for wifi_save in get_wifis_saves:
                    if wifi[0].decode() == wifi_save["wifi"]:
                        return wifi_save["wifi"], wifi_save["password"]
                    
        return autocon
        
        
    def wifis_scans(self)->list[tuple]:
        justScan = SettingsInternet()
        return justScan.network_scans_around()
       
       
    def socket_accept(self):
        return self.server.socket_accept()
        
        
