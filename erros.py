

#Classe para erros inexperados de tentativa de iniciar o WLAN
class ErroWLAN(Exception):
    
    def __init__(self, mensage:str ="Erro inexperado interno, verifique o estado do microcontrolador e o firmwar"):
        
        self.erro_menssage = mensage
        
    def pin_error(self):
         print(self.erro_menssage)
         return False

