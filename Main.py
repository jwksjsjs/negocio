from internet import MakerConnection
import web
import grafico#funcao em c++


#Classe de intermédio entre o front e o back
class Main:
   
    def __init__(self, internetName=None, password=None):
        self.internetName = internetName
        self.password = password
        self.serverToken = MakerConnection(self.internetName, self.password)
        self.serverSocket = self.serverToken.begin_socket()
       
    def run_app(self):    
       #iniciar o servidor em internet.py    
       
        
        self.severConnection = self.serverToken.begin_connection()
       
       #chamar o módulo web.py
       #runWeb = web.home_page
       #runWeb()
             
       #pegar as informacoes de rede
       #a funcao set_internet_user vai ser chamada pelo módulo web
       
       
  #mandar as informações de rede pra interne.py  
       #Server.beggin_connection(internetName, password)
       #vai ser chamada pela web
       
       #pegar as informacoes de web.py de volume         #chamar o módulo .c
       #mandar as informções de volume codigo pro módulo .c
       
       #pegar o gráfico gerado pelo módulo em c
       #enviar pra web o gráfico vindo de c
    def conector(self):
        serverAcception, addrServerAcception = self.serverToken.socket_accept()
        return serverAcception, addrServerAcception
       
       
    def wifis_scans(self):          
        wifiScans = self.serverToken.get_scans()
        return wifiScans
       
       
    def set_sound(self, sound):
        pass
        #chamar a funcao c++
       
    def set_grafic(self):
        pass
        #chama o gráfico em c++ e repassa pra web
       
    def config_autoconnection(self, setAuto):
        self.serverToken.is_autoconnection(setAuto)
        
    
    def auto_login(self):
        return self.serverToken.make_autoconnection()
        #boolenao True or False, redireciona a home_page caso True
       
if __name__ == "__main__":
   
    try:
        runner = main()
        runner.run_server()
       
       
    except:
        exit() #web.tela_de_erro(


