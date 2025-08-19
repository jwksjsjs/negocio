import uasyncio as asyncro
import machine 
from machine import Pin
               
#============DEFINE O PINO DE LED E SUAS FUNCIONALIDADES============#              
class PinLed:
    
    STATUS_PIN_1 = 2
    WAIT = 0.5
    
    def __init__(self)->None:
        self.LED = Pin(PinLed.STATUS_PIN_1, Pin.OUT)
   
    @property
    def led(self)->Pin:
        return self.LED

    async def led_on(self)->None:
        self.led.on()
        await asyncro.sleep(PinLed.WAIT)
       
    async def led_off(self)->None:
        self.led.off()
        await asyncro.sleep(PinLed.WAIT)

    async def loop_led(self)->None:
        while True:
            await self.led_on()
            await self.led_off()
           
    def __str__(self)->str:
        return str(self.led)


#=============DEFINE O BOTÃO DE RESET E SUAS FUNCIONALIDADES=================#
class PinReset:
    
    PIN_RESET = 13
    
    def __init__(self)->None:
        self._reset_button = Pin(PinReset.PIN_RESET, Pin.IN, Pin.PULL_UP)
        self.reset_alert = PinLed()
        self.TIMER_RESET = 0
        
    @property
    def reset_button(self)->Pin:
        return self._reset_button    
   
    #FUNÇÃO DE RESET, SE O BOTÃO DE RESET FOR APERTADO DURANTE
    #2.5 SEGUNDOS ACONTECE O RESET, CASO CONTRÁRIO NADA ACONTECE
    async def press_reset(self)->bool:
        led_task = None
        reset = False
        
        while self._reset_button.value() == 0:
            
            if self.TIMER_RESET == 0:
                led_task = asyncro.create_task(self.reset_alert.loop_led())
            elif self.TIMER_RESET == 5:
                reset = True
                machine.reset()
                break
                
            await asyncro.sleep(0.5)
            self.TIMER_RESET += 1

        if led_task: led_task.cancel()
        await self.reset_alert.led_off()
    
        return reset

    async def check_reset(self):
        check = False
        while not check:
            check = self.press_reset()
            await asyncro.sleep(0.5)
          
        return check
  
    def __str__(self)->str:
        return str(self.reset_button)

