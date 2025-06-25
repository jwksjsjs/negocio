
import random
import matplotlib.pyplot as mp
import numpy as np


#========DEIXEM SEMPRE 2 LINHAS AO FINAL DE FUNÇÕES E 3 LINHAS AO FINAL DE CLASSES PELO AMOR DE DEEEEEUS=========
#MÓDULO DE REFERNCIA PARA TRADUÇÃO EM C++


WAIT_DRAW_NEW_PLOT = 0.05


#classe opcional, apenas exibe elementos gráficos
class Grafic:
   
    def __init__(self):      
        #opcionais===============
        self.xName = "Tempo"
        self.yName = "Frequencia"    
        self.graficTitle = "Gráfico de frequencia"
        self.graficColor= "g"
        self.graficLabelLine = "Variação da frequencia em função do tempo"            
        #=======================        


    """funcao opcinal da classe Grafic, mas precisa ser implementada diretamente em
    GeneratedGrafic caso a classe Grafic deixe de existir"""
    def craft_design_grafic(self, ax):        
             
        ax.set_xlabel(self.xName)
        ax.set_ylabel(self.yName)
        ax.set_title(self.graficTitle)
        ax.grid(True)
        ax.legend()
                 
                 


class GeneratedGrafic(Grafic):
       
    def __init__(self, xValue, yValue):            
        super().__init__()
       
        self.fullGraficSize, self.dynamicGraficSize = self.real_time_grafic()
       
        #isso provavelmente vai mudar, dependendo de como vai vir os nwgocio==================
        self.x = [xValue]
        self.y = [np.sin(yValue*0.1)]      
        #===============================
       
        self.line = self.dynamicGraficSize.plot(self.x, self.y, color = self.graficColor, label = self.graficLabelLine)[0]    
       
        #isso vai sair =======
        self.a = 0
        self.g = self.gerador()
        #=================
       
    #isso tbm vai sair ===========
    def gerador(self):              
        g = (n for n in range(1_000))
       
        return g
   #==============================
       
    def conversion_data(self):
        pass
        #aqui vai ser a função que vai aplicar o cálculo pra deixar em formato senoidal
       
       
    def real_time_grafic(self):
        mp.ion()
        figure, ax = mp.subplots()
       
        return figure, ax


       
    def get_data(self):  
        #isso vai mudar=======
        for i in range(10):
         
           try:
                _next = next(self.g)
                v = (np.sin(_next*random.randint(1, 100)))
                self.x.append(_next+self.a)
                self.y.append(v)        
           except:
                self.g = self.gerador()
                self.a += 1_000
        #====================


    def real_time_grafic_config(self):        
       
        self.get_data()
        self.line.set_xdata(self.x)
        self.line.set_ydata(self.y)
        self.dynamicGraficSize.relim()
        self.dynamicGraficSize.autoscale_view()
        self.craft_design_grafic(self.dynamicGraficSize)
       
       
    def real_time_grafic_run(self):


        while True:


            self.real_time_grafic_config()
            mp.draw()
            mp.pause(WAIT_DRAW_NEW_PLOT)            


        mp.ioff()
        mp.show()


       
#isso vai ser instanciado por uma interface externa que vai importar a classe gerneratedGrafic
x = 1
y = 9
G = GeneratedGrafic(x, y)                      
G.real_time_grafic_run()
#=======================



#=================================