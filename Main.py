from internet import MakerConnection, SettingsInternet
import web
import grafico#funcao em c++

#nao sei como tá a identificação já que nao tem tab disponível
#Classe de intermédio entre o front e o back, tem que ser equeno, vai so chamar as coisas
class Main:
   
    def __init__(self, internetName=None, password=None):
        self.internetName = internetName
        self.password = password
        self.serverToken = MakerConnection(self.internetName, self.password)
        self.serverSocket = self.serverToken.begin_socket()
       
    def run_app(self):    
       #iniciar o servidor em internet.py
        if 
        self.severConnection = self.serverToken.begin_connection()
        self.connectedIn = self.serverToken.socket_accept()
        clientSever = {"Id": internetName,
                       "Servidor": self.connecteIn[0]}
       
        return clientServer
       
       
    def wifis_around(self):
       #isso vai ser uma lista ou tupla de um monte de redes, tem que
        wifisAround = self.serverToken.wifis_scans()
        wifis = [{"Rede": Wifi[0].decode(), "Potência do sinal": Wifi[3]} for Wifi in wifisAroud]
        return wifis
       
       
    def set_sound(self, sound):
        pass
        #chamar a funcao c++
       
    def set_grafic(self):
        pass
        #chama o gráfico em c++ e repassa pra web
       
    def config_autoconnection(self, setSelfConn):
        self.serverToken.is_selfconnection(setSelfConn)
        
    
    def auto_login(self):
        
        datasToSelfConn= self.serverToken.make_selfconnection()
        #usa if pra verificar False, se False retorna pra uma pagina html de erro
        #ou avisando que nao conseguiu se conectar, tem que ver como diferenciar
        if datasToSelfConn:
            self.internetName, self.password = datasToSelfConn[0], datasToSelfConn[1]
            self.serverToken = MakerConenction(self.internetName, self.password)
            self.run_app()


        return False
       #seta a conexão automática, mas tem que impedir que isso ocorra caso a
       #internet ja estaja conetada
       #web.py vai chamar isso aqui e fazer o resto com a resposta
       
       
if __name__ == "__main__":
    try:
        runner = main()   
    except:
        return 0


