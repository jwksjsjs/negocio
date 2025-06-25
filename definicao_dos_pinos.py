from machine import Pin, Timer, I2C
import socket as sck




#MÓDULO QUASE EXCLUSUVO DO MÓDULO C++, TODAS ESSAS MATERIALIZAÇÕES SÃO CRIADAS PRA MANIPULAÇÃO DO CÓDIO EM C++,
#COM EXCESSÃO DE SOCKETS QUE TAMBÉM SERÁ USADA POR INTERNET.PY
class Pins:
   
    PIN_SDA = 21
    PIN_SCL = 22
    PIN_RESET = 13
    STATUS_PIN = 2
     
    @property
    def pin_sda(self)->int:
        return self.PIN_SDA


    @property
    def pin_scl(self)->int:
        return self.PIN_SCL


    @property
    def pin_reset(self)->int:
        return self.PIN_RESET


    @property
    def led_status(self)->int:
        return self.STATUS_PIN


   


class PinReset(Pins):
   
    def __init__(self)->None:
        super().__init__()
        self._reset_button = Pin(self.pin_reset, Pin.IN, Pin.PULL_UP)


    @property
    def reset_button(self)->Pin:
        return self._reset_button
       
       
    def __str__(self)->str:
        return str(self.reset_button)
               
               
               
class PinLed(Pins):
       
    def __init__(self)->None:
        super().__init__()
        self.ledStatus = Pin(self.led_status, Pin.OUT)      
       
    @property
    def led(self)->Pin:
        return self.ledStatus
 
   
    def __str__(self)->str:
        return str(self.led)
 
 
 
class BarramentI2C(Pins):
   
    BARRAMENT_1_I2C = 0
    BARRAMENT_2_I2C = None
   
    def __init__(self)->None:
        super().__init__()
        self._i2c = I2C(BarramentI2C.BARRAMENT_1_I2C, scl = Pin(self.pin_scl), sda = Pin(self.pin_sda))
       
       
    @property
    def barrament_i2c(self)->I2C:
        return self._i2c
   
   
    def __str__(self)->str:
        return str(self.barrament_i2c)
 
     
     
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



