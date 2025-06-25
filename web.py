import main
from flask import Flask


app = Flask(__name__)
import socket
import network






#>>>>>ISSO NÃO VAI USAR FLASK, MAS EU PRECISO DELE PRA RODAR COMO SERVER
def get_redes_html():
    redes = main.wifis_scans()
    lista = ''.join([f'<li>{str(red[0], "utf-8")}</li>' for red in redes])
    return f"""
    <html>
        <head><title>Redes Wi-Fi</title></head>
        <body>
            <h1>Redes Wi-Fi disponíveis:</h1>
            <ul>{lista}</ul>
        </body>
    </html>
    """




def start_web_server():
     
    while True:
        conn, addr = main.conector()
       
        print('Conexão de', addr)
        request = conn.recv(1024)
        response = get_redes_html()
        conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()
       
       
       
@app.route("/")
def return_home_page():
   
    with open("telas.html", "r") as F:
        return F.read()




@app.route("/config")
def return_tela_config():
    with open("tela_configuracao.html", "r") as F:
        return F.read()


#Funcao pra pegar e enviar as redes próximas
         
def redirect_templates():
    pass
    #se a rota for nula, redirecionar pra as informações de rede
   
    #pegar as informações de rede vindas de um POST do front e mandar pra main.py    
     
     #pegar as iformacoes de volume vindas de um POST do front e mandar pra main.py
     
     #enviar o gráfico vindo de main.py pro front
   
   
app.run()    



