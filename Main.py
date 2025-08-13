from internet import MakerConnection
from defspins import PinReset
import web
import grafico  # função em C++
import uasyncio as asyncro


class Main:
    PORT = 80
    IP = "0.0.0.0"

    def __init__(self, internetName: str = None, password: str = None) -> None:
        self.internetName = internetName
        self.password = password
        self.serverToken = MakerConnection(self.internetName, self.password)
        self.reset = PinReset()

        self.task_grafic = None
        self.task_sound = None
        self.task_resetPin = None
        self.task_checkInternet = None

    #inicia o servidor assincrono
    async def begin_server(self):
        await asyncro.start_server(self.requests_route, self.IP, self.PORT)

    
    def check_task(self, task, exe):
        if task is None:
            return asyncro.create_task(exe())
        return task

    
    async def requests_route(self, reader, writer):
        #Tem que cancelar as funções assincronas quando sair da tela de
        #config ou quando sair da apl
        while True:
            #fazer check  pin e check  internet
            self.task_resetPin = self.check_task(self.task_resetPin, self.check_resetPin)
            self.task_checkInternet = self.check_task(self.task_checkInternet, self.serverToken.check_internet)
            
            line = await reader.readline()
            requestPage = line.decode().split(" ")[1]

            if requestPage == "/":
                selfLog = self.self_login()
                if not selfLog:
                    # enviar mensagem de falha de conexão
                    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nFalha ao conectar")
                    await writer.drain()
                else:
                    # renderizar página
                    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nConectado com sucesso")
                    await writer.drain()

            elif requestPage.startswith("/config"):
                #fazer check grafic e check sound
                self.task_grafic = self.check_task(self.task_grafic, self.check_grafic)
                self.task_sound = self.check_task(self.task_sound, self.check_sound)
                #set sound

                if "=" in requestPage:
                    dataValue = requestPage.split("=")[1]
                    print("Valor de configuração:", dataValue)

            await writer.aclose()

    
    def run_app(self) -> dict:
        self.serverConnection = self.serverToken.begin_connection()
        self.connectedIn = self.serverToken.socket_accept()
        return {"Id": self.internetName, "Servidor": self.connectedIn[0]}

    
    def wifis_around(self) -> list[dict]:
        wifisAround = self.serverToken.wifis_scans()
        return [{"Rede": _wifi_[0].decode(), "Potência do sinal": _wifi_[3]} for _wifi_ in wifisAround]

    #define se vai ser autoconectavel, não está sendo usado, precisa colocar na tella de início
    def config_selfconnection(self, setSelfConn: bool = False) -> None:
        self.serverToken.is_selfconnection(setSelfConn)

    
    def self_login(self) -> bool:
        datasToSelfConn = self.serverToken.make_selfconnection()
        if datasToSelfConn:
            self.internetName, self.password = datasToSelfConn
            self.serverToken = MakerConnection(self.internetName, self.password)
            self.run_app()
            return True
        return False
        

if __name__ == "__main__":
    try:
        runner = Main()
        asyncro.run(runner.begin_server())
    except Exception as e:
        print('Erro ao iniciar o servidor:', e)
