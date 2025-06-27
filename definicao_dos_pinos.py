from machine import Pin
from time import sleep
import socket as sck

class PinReset(Pins):
    PIN_RESET = 13
    def __init__(self)->None:
        self._reset_button = Pin(PinReset.PIN_RESET, Pin.IN, Pin.PULL_UP)

    @property
    def reset_button(self)->Pin:
        return self._reset_button   
       
    def __str__(self)->str:
        return str(self.reset_button)
               
               
class PinLed:
   
    STATUS_PIN_1 = 2
    #STATUS_PIN_2 = None
    def __init__(self)->None:
        self.LED = Pin(PinLed.STATUS_PIN, Pin.OUT)
   
    @property
    def led(self)->Pin:
        return self.LED

    def led_on(self)->None:
        self.led.on()
        sleep(1.5)
       
    def led_off(self)->None:
        self.led.off()
        sleep(1.5)

    def loop_pin(self, arg:bool = False)->None:
       #nao vai ser desligado aqui
        while arg:
            self.led_on()
            self.led_off()
           
        return 
                   
    def __str__(self)->str:
        return str(self.led)
     
class Sockets:
   
    IP_CONECTION = "0.0.0.0"
    PIN_HTTP = 80
    SOCKET_LISTEN = 1
   
    def __init__(self)->None:
        self.socket_ = self.config_socket()
       
           
    def config_addr(self)->tuple:
        addr = sck.getaddrinfo(Sockets.IP_CONECTION, Sockets.PIN_HTTP)[0][-1]
        return addr
           
   
    def config_socket(self)->sck.socket:    
        self.socketAddr = self.config_addr()
        socket_ = sck.socket()
        socket_.bind(self.socketAddr)
        socket_.listen(Sockets.SOCKET_LISTEN)    
        return socket_
   
           
    def socket_accept(self)->tuple:
        conn, addr = self.socket_.accept()  
        return conn, addr
       
       
    def __str__(self)->str:
        return str(self.socket_)



