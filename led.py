from gpiozero import RGBLED
from time import sleep

#list constants for the colors
RED = (0,1,1)
BLUE = (1,1,0)
GREEN = (1,0,1)
WHITE = (0,0,0)
CYAN = (1,0,0)
PURPLE = (0,1,0)
OFF = (1,1,1)

led = RGBLED(27,17,18,active_high=False)

#functions that sets the light as certain conditions
def green():
    led.color = GREEN

def red():
    led.color = RED
    sleep(1)

def blue():
    led.color = BLUE
    
def flashing():
    for i in range(1):
        led.color = WHITE
        sleep(0.25)
        led.color = CYAN
        sleep(0.25)
        led.color = BLUE
        sleep(0.25)
        led.color = GREEN
        sleep(0.25)
        led.color = PURPLE
        sleep(0.25)
        led.color = RED
        sleep(0.25)
    off()
        
def off():
    led.color = OFF