import network as net
import ujson
from erros import ErroWLAN, ConnectionError
from time import sleep
import uasyncio as asyncro
#Esse arquivo tá finalizado eu não vou mexer nisso de novo por nada nesse mundo

#>>>>>>>>>>>DEIXEM 2 LINHAS ENTRE DEFS E 3 ENTRE CLASSES<<<<<<<<<<<<#

#====================INICIA O WIFI DO ESP32 E=========================#
#=======TENTA FAZER A CONEXÃO COM A REDE FORNECIDA PELO USUÁRIO=======#
class SettingsInternet:  
    
    def __init__(self, nameNetwork=None, keyNetwork=None)->None:
        self._nameNetwork = nameNetwork
        self._keyNetwork = keyNetwork
        self.wifi = None
        
    #TENTA ATIVAR O WIFI DO ESP32 OU GERA UM ERRO
    def activate_network(self)->bool:
        try:
            self.wifi = net.WLAN(net.STA_IF)
            self.wifi.active(True)
            return True
            
        except Exception:
            fatal_error = ErroWLAN()
            return fatal_error.pin_error()


    #VERIFICA SE O WIFI ESTÁ CONECTADO A UMA REDE. SE NÃO ESTIVER, TENTA SE CONETAR
    #COM A REDE ESCOLHIDA PELO USUÁRIO USANDO DAS INFORMAÇÕES DADAS POR ELE
    def verif_conn(self)->None:       
       if not self.wifi.isconnected():
           self.wifi.connect(self._nameNetwork, self._keyNetwork)
    
    #RESPONSAVEL POR CHAMAR AS DUAS DEFS ACIMA E GERAR UM ERRO CASO NÃO CONSIGA SE
    #CONECTAR A UMA REDE
    async def connect_network(self)->bool:
        if self.activate_network():
            self.verif_conn()
            try:
                for _ in range(10):
                    if self.wifi.isconnected():
                        return True    
                    await asyncro.sleep(1)
                raise ConnectionError()
                
            except ConnectionError as e:
                connect_net_error = e.password_error()
                return connect_net_error

    #VERIFICA TODAS AS REDES DISPONÍVEIS AO ENTORNO
    def network_scans_around(self)->list[tuple] | None:
        wifis_scans = self.wifi.scan()
        return wifis_scans if wifis_scans else None


#======SALVA AS INFORMAÇÕES DO USUÁRIO E AS RETORNA QUANDO NECESSÁRIO======#
class ManagerWifiInfor:
   
    def __init__(self, wifiName, password)->None:
        self._wifiName = wifiName
        self._password = password

    #GERA UM DICIONÁRIO COM OS DADOS DA REDE
    def data_wifi(self)->dict[str, str]:
        return {"wifi": self._wifiName, "password": self._wifiPassword}

    #RETORNA UM JSON ABERTO
    def read_json_wifis(self, file):
        try:
            with open(file, "r") as j:
                return ujson.load(j)
        
        except (OSError, ValueError):
            print(f"Erro ao ler o arquivo: {file}")
            return None
    
    #ESCREVE DADOS EM UM ARQUIVO JSON
    def whrite_json_wifis(self, file, data)->None:
        with open(file, 'w') as j:
            ujson.dump(data, j)
             
    #SALVA AS INFORMAÇÕES DA REDE APÓS TER SIDO POSSÍVEL SE CONETAR COM ELA
    #E CASO A REDE AINDA NÃO ESTEJA SALVA NO ARQUIVO JSON
    def save_wifi_info(self) -> None:
        jsonOppen = self.all_wifis()
        if jsonOppen is None:
            self.whrite_json_wifis("list_wifis.json", [self.data_wifi()])
            return

        for savedWifi in jsonOppen:
            if savedWifi["wifi"] == self._wifiName:
                return

        jsonOppen.append(self.data_wifi())
        self.whrite_json_wifis("list_wifis.json", jsonOppen)      

    #RETORNA TODOS OS WIFIS SALVOS 
    def all_wifis(self)->list[dict()] | None:
        wifi_list = self.read_json_wifis('list_wifis.json')
        return wifi_list

    #SALVA SE O USUÁRIO QUER OU NÃO SE CONETAR AUTOMATICAMENTE
    #A REDES JÁ ANTES ACESSADAS
    def set_selfconnection(self, response)->None:
        with open('autologin.json', "w") as j:
            ujson.dump({"autoconexão": response}, j)
        
    #RETORNA SE O USUÁRIO QUED OU NAO SE CONETAR AUTOMATICAMENTE  
    def return_selfconnection(self)->bool:
        with open('autologin.json', "r") as j:
            isauto = ujson.load(j)
            return isauto["autoconexão"]



#==========RECEBE AS INFORMAÇÕES FORNECIDAS PELO USUÁRIO===========#
#======USA DESSAS INFORMAÇÕES PARA CHAMAR AS CLASSES A CIMA========#

class MakerConnection:
   
    def __init__(self, internetName:str, password)->None:
        self.internetName = internetName
        #nao acho que crip é necessário 
        self.password = password
        self.w = ManagerWifiInfor(self.internetName, self.password)

    #CHAMAS AS FUNCOES QUE PERMITEM ATIVAR O WIFI DO ESP32 E LOGAR NUM REDE
    async def begin_connection(self)->bool:          
        self.internetServer = SettingsInternet(self.internetName, self.password)
        self.connection = await self.internetServer.connect_network()
        
        if self.connection:
            self.w.save_wifi_info()
       
        return self.connection
       
    #REPASSA A INFORMAÇÃO DE AUTOCONEXÃO PARA SALVAMENTO EM JSON
    def define_selfconnection(self, autoconn)->None:
        self.w.set_selfconnection(autoconn)
        
    #CHAMA A FUNÇÕES QUE VERIFICAM SE O USUÁRIO QUER SE AUTOCONECTAR E AS REDES PRÓXIMAS,
    #COM BASE NISSO ACESSA SUA MEMÓRIA PARA FAZER AUTOCONEXÃO OU NÃO COM REDES ANTES SALVAS
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
        
    #CHAMA A FUNÇÃO QUE VERIFICA REDES PRÓXIMAS E A RETORNA
    def wifis_scans(self)->list[tuple]:
        justScan = SettingsInternet()
        return justScan.network_scans_around()

    def check_internet(self)->bool:
        return self.internetServer.wifi.isconnected()
        
