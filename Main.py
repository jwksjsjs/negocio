from internet import MakerConnection
from defspins import PinReset
from Aundio import soundNull
import uasyncio as asyncro

def read_html(path: str):
    """Lê um arquivo e retorna seu conteúdo (ou None se não existir)."""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        print("read_html erro:", e)
        return None
        
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

            if not self.task_checkInternet:
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
                
            elif requestPage.startswith("/reconnect"):
                ok = self.serverToken.begin_connection() if not hasattr(self.serverToken, "begin_connection") else self._call_begin_async(self.serverToken)
                # alguns MakerConnection podem ter begin_connection como coroutine ou função;
                # aqui só respondemos informando que a ação foi recebida
                await self._write_response(writer, 200, "application/json", '{"reconnect": true}')

            else:
                    await self._write_response(writer, 404, "text/plain", "Not found")
           
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

    
    async def _write_response(self, writer, status_code: int, content_type: str, body: str):
        """Escreve cabeçalho e corpo (string) e faz drain."""
        try:
            header = "HTTP/1.1 %d OK\r\nContent-Type: %s\r\nContent-Length: %d\r\n\r\n" % (status_code, content_type, len(body))
            writer.write(header.encode())
            writer.write(body.encode())
            await writer.drain()
        except Exception as e:
            print("Erro escrevendo response:", e)
    
    
    def _call_begin_async(self, serverToken):
        try:
            c = serverToken.begin_connection()
            # se for coroutine, agende
            if hasattr(c, "__await__"):
                asyncro.create_task(c)
            return True
        except Exception as e:
            print("Erro ao chamar begin_connection:", e)
            return False


async def _boot():
    runner = Main()
    await runner.begin_server()


if __name__ == "__main__":
    try:
        asyncro.run(_boot())
    except Exception as e:
        print('Erro ao iniciar o servidor:', e)
