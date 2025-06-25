
#Tudo vai ser bem simpleszinho
#Classe para erros inexperados de tentativa de iniciar o WLAN
class WLAMErroException):
    
    def __init__(self, mensage:str ="Erro inexperado interno, verifique o estado do microcontrolador e o firmwar"):     
        self.erroMensage = mensage
        
    def pin_error(self)->bool:
         print(self.erroMensage)
         return False


class ConnectionError(Exception):
    def __init__(self, mensage:str = "senha incorreta")->None:
        self.erroMensage = mensage

    def password_error(self)->bool:
        print(self.erroMensage)
        return False
        
        
class UnexpectedError(Exception):
    def __init__(self)->None:
        self.erroMensage = "Erro inexperado"

    def error(self)->bool:
        print(self.erroMensage)
        return False
    








