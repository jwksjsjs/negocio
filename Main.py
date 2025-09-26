from internet import MakerConnection
from defspins import PinReset
from Aundio import soundNull
import uasyncio as asyncro

def read_html(args):
    try:
        with open(args) as f:
            return read(f)
    except:
        return #RECHARGE

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

    # inicia o servidor assíncrono
    async def begin_server(self):
        await asyncro.start_server(self.requests_route, self.IP, self.PORT)

    def check_task(self, task, exe):
        if task is None:
            return asyncro.create_task(exe())
        return task

    async def requests_route(self, reader, writer):
        while True:
            # checar pino de reset e internet
            self.task_resetPin = self.check_task(self.task_resetPin, self.reset.check_reset)
            self.task_checkInternet = self.check_task(self.task_checkInternet, self._check_internet_task)

            if not self.task_checkInternt:
                #redireciona para uma pgina html de erro de conexão
            #if not self.task_resetPin:
            #faz alguma coisa dependendo da finalidade do pin

            line = await reader.readline()
            if not line:
                break
            parts = line.decode().split(" ")
            if len(parts) < 2:
                break
            requestPage = parts[1]

            # consumir cabeçalho até linha em branco
            while True:
                hl = await reader.readline()
                if not hl or hl == b"\r\n":
                    break

            if requestPage == "/":
                selfLog = self.self_login()
                if not selfLog:
                    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nFalha ao conectar")
                    await writer.drain()
                else:
                    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nConectado com sucesso")
                    await writer.drain()

            elif requestPage.startswith("/config"):
                # tarefas auxiliares (stubs)
                self.task_grafic = self.check_task(self.task_grafic, self.check_grafic)
                self.task_sound = self.check_task(self.task_sound, self.check_sound)

                # set sound via query ?value=...
                if "=" in requestPage:
                    dataValue = requestPage.split("=", 1)[1]
                    print("Valor de configuração:", dataValue)

                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nOK")
                await writer.drain()

            try:
                await writer.wait_closed()
            except AttributeError:
                # compatibilidade com versões antigas
                pass
            break

    async def _check_internet_task(self):
        while True:
            _ = self.serverToken.check_internet()
            await asyncro.sleep(2)

    def run_app(self) -> dict:
        # agenda a tentativa de conexão (sem bloquear)
        asyncro.create_task(self.serverToken.begin_connection())
        return {"Id": self.internetName or "", "Servidor": True}

    def wifis_around(self):
        wifisAround = self.serverToken.wifis_scans()
        if not wifisAround:
            return []
        return [{"Rede": _wifi_[0].decode() if isinstance(_wifi_[0], bytes) else _wifi_[0],
                 "Potência do sinal": _wifi_[3]} for _wifi_ in wifisAround]

    # define se vai ser autoconectável (não usado na tela inicial)
    def config_selfconnection(self, setSelfConn: bool = False) -> None:
        self.serverToken.define_selfconnection(setSelfConn)

    def self_login(self) -> bool:
        datasToSelfConn = self.serverToken.make_selfconnection()
        if datasToSelfConn and isinstance(datasToSelfConn, tuple):
            self.internetName, self.password = datasToSelfConn
            self.serverToken = MakerConnection(self.internetName, self.password)
            # agenda conexão
            asyncro.create_task(self.serverToken.begin_connection())
            return True
        return False


async def _boot():
    runner = Main()
    await runner.begin_server()


if __name__ == "__main__":
    try:
        asyncro.run(_boot())
    except Exception as e:
        print('Erro ao iniciar o servidor:', e)
