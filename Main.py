from internet import MakerConnection
import web
import grafico#funcao em c++


#Classe de intermédio entre o front e o back, tem que ser equeno, vai so chamar as coisas
class Main:
   
    def __init__(self, internetName=None, password=None):
        self.internetName = internetName
        self.password = password
        self.serverToken = MakerConnection(self.internetName, self.password)
        self.serverSocket = self.serverToken.begin_socket()
       
    def run_app(self):    
       #iniciar o servidor em internet.py
        self.severConnection = self.serverToken.begin_connection()
       
    def conector(self):
        serverAcception, addrServerAcception = self.serverToken.socket_accept()
        return serverAcception, addrServerAcception
       
       
    def wifis_around(self):          
        wifiScans = self.serverToken.wifis_scans()
        return wifiScans
       
       
    def set_sound(self, sound):
        pass
        #chamar a funcao c++
       
    def set_grafic(self):
        pass
        #chama o gráfico em c++ e repassa pra web
       
    def config_autoconnection(self, setAuto):
        self.serverToken.is_selfconnection(setAuto)
        
    
    def auto_login(self):

        self.internetName, self.password = self.serverToken.make_selfconnection()
        #usa if pra verificar False, se False retorna pra uma pagina html de erro
        #ou avisando que nao conseguiu se conectar, tem que ver como diferenciar
       
        self.serverToken = MakerConenction(self.internetName, self.password)
       #seta a conexão automática, mas tem que impedir que isso ocorra caso a
       #internet ja estaja conetada
       #web.py vai chamar isso aqui e fazer o resto com a resposta
       
       
if __name__ == "__main__":
   
    try:
        runner = main()
        runner.run_server()
       
       
    except:
        exit() #web.tela_de_erro(


