import network as net
import ujson
from erros import ErroWLAN, ConnectionError
import uasyncio as asyncro


#====================INICIA O WIFI DO ESP32 E=========================#
#=======TENTA FAZER A CONEXÃO COM A REDE FORNECIDA PELO USUÁRIO=======#
class SettingsInternet:

    def __init__(self, nameNetwork=None, keyNetwork=None) -> None:
        self._nameNetwork = nameNetwork
        self._keyNetwork = keyNetwork
        self.wifi = None

    # TENTA ATIVAR O WIFI DO ESP32 OU GERA UM ERRO
    def activate_network(self) -> bool:
        try:
            self.wifi = net.WLAN(net.STA_IF)
            self.wifi.active(True)
            return True
        except Exception:
            fatal_error = ErroWLAN()
            return fatal_error.pin_error()

    # VERIFICA SE O WIFI ESTÁ CONECTADO; SENÃO, TENTA CONECTAR
    def verif_conn(self) -> None:
        if not self.wifi.isconnected():
            self.wifi.connect(self._nameNetwork, self._keyNetwork)

    # CHAMA AS DUAS DEFS ACIMA E GERA ERRO CASO NÃO CONSIGA CONECTAR
    async def connect_network(self) -> bool:
        if self.activate_network():
            self.verif_conn()
            try:
                for _ in range(10):
                    if self.wifi.isconnected():
                        return True
                    await asyncro.sleep(1)
                raise ConnectionError()
            except ConnectionError as e:
                return e.password_error()
        return False

    # VERIFICA TODAS AS REDES DISPONÍVEIS
    def network_scans_around(self):
        # Garante interface ativa para scan mesmo quando chamada isolada
        if self.wifi is None:
            try:
                self.wifi = net.WLAN(net.STA_IF)
                self.wifi.active(True)
            except Exception:
                return None
        scans = self.wifi.scan()
        return scans if scans else None


#======SALVA AS INFORMAÇÕES DO USUÁRIO E AS RETORNA QUANDO NECESSÁRIO======#
class ManagerWifiInfor:

    def __init__(self, wifiName, password) -> None:
        self._wifiName = wifiName
        self._password = password

    # GERA UM DICIONÁRIO COM OS DADOS DA REDE
    def data_wifi(self):
        return {"wifi": self._wifiName, "password": self._password}

    # RETORNA UM JSON ABERTO
    def read_json_wifis(self, file):
        try:
            with open(file, "r") as j:
                return ujson.load(j)
        except (OSError, ValueError):
            print("Erro ao ler o arquivo:", file)
            return None

    # ESCREVE DADOS EM UM ARQUIVO JSON
    def whrite_json_wifis(self, file, data) -> None:
        with open(file, 'w') as j:
            ujson.dump(data, j)

    # SALVA AS INFORMAÇÕES DA REDE APÓS CONECTAR (SE NÃO EXISTIR)o
    def save_wifi_info(self) -> None:
        jsonOppen = self.all_wifis()
        if jsonOppen is None:
            self.whrite_json_wifis("list_wifis.json", [self.data_wifi()])
            return

        for savedWifi in jsonOppen:
            if savedWifi.get("wifi") == self._wifiName:
                return

        jsonOppen.append(self.data_wifi())
        self.whrite_json_wifis("list_wifis.json", jsonOppen)

    # RETORNA TODOS OS WIFIS SALVOS
    def all_wifis(self):
        return self.read_json_wifis('list_wifis.json')

    # SALVA PREFERÊNCIA DE AUTOCONECTAR
    def set_selfconnection(self, response) -> None:
        with open('autologin.json', "w") as j:
            ujson.dump({"autoconexão": bool(response)}, j)

    # RETORNA PREFERÊNCIA DE AUTOCONECTAR
    def return_selfconnection(self) -> bool:
        try:
            with open('autologin.json', "r") as j:
                isauto = ujson.load(j)
                return bool(isauto.get("autoconexão", False))
        except (OSError, ValueError):
            return False


#==========RECEBE AS INFORMAÇÕES FORNECIDAS PELO USUÁRIO===========#
#======USA DESSAS INFORMAÇÕES PARA CHAMAR AS CLASSES A CIMA========#
class MakerConnection:

    def __init__(self, internetName: str, password) -> None:
        self.internetName = internetName
        self.password = password
        self.w = ManagerWifiInfor(self.internetName, self.password)
        self.internetServer = None
        self.connection = False

    # ATIVA WIFI DO ESP32 E LOGA NA REDE
    async def begin_connection(self) -> bool:
        self.internetServer = SettingsInternet(self.internetName, self.password)
        self.connection = await self.internetServer.connect_network()
        if self.connection:
            self.w.save_wifi_info()
        return self.connection

    # SALVA PREFERÊNCIA DE AUTOCONECTAR
    def define_selfconnection(self, autoconn) -> None:
        self.w.set_selfconnection(autoconn)

    # FAZ AUTOCONEXÃO COM REDES SALVAS SE DISPONÍVEIS
    def make_selfconnection(self):
        autocon = self.w.return_selfconnection()
        if autocon:
            get_wifis_saves = self.w.all_wifis()
            available_wifis = self.wifis_scans()

            if not get_wifis_saves or not available_wifis:
                print("Nenhuma rede salva para tentar conexão automática.")
                return False

            for wifi in available_wifis:
                ssid = wifi[0].decode() if isinstance(wifi[0], bytes) else wifi[0]
                for wifi_save in get_wifis_saves:
                    if ssid == wifi_save.get("wifi"):
                        return wifi_save["wifi"], wifi_save["password"]
        return autocon

    # RETORNA SCAN DE REDES
    def wifis_scans(self):
        justScan = SettingsInternet()
        return justScan.network_scans_around()

    # CHECA SE ESTÁ CONECTADO (ROBUSTO SE AINDA NÃO CHAMOU begin_connection)
    def check_internet(self) -> bool:
        try:
            return bool(self.internetServer and self.internetServer.wifi and self.internetServer.wifi.isconnected())
        except Exception:
            return False
