import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

directionx = 22 # Direction (DIR) GPIO Pin
stepx = 23 # Step GPIO Pin
EN_pin_x = 24 # enable pin (LOW to enable)

directiony = 26
stepy = 19
EN_pin_y = 13


motorx = RpiMotorLib.A4988Nema(directionx, stepx, (21,21,21), "DRV8825")
GPIO.setup(EN_pin_x,GPIO.OUT)

motory = RpiMotorLib.A4988Nema(directiony, stepy, (21, 21, 21), "DRV8825")
GPIO.setup(EN_pin_y, GPIO.OUT)

#Y is 8900 long
GPIO.output(EN_pin_y, GPIO.LOW)
motory.motor_go(False, "1/4", 2000, 0.00002, False, 0.05)

#X is 11550 long
GPIO.output(EN_pin_x, GPIO.LOW)
motorx.motor_go(False, "1/4", 2000, 0.00002, False, 0.05)


GPIO.output(EN_pin_y,GPIO.HIGH)
GPIO.output(EN_pin_x, GPIO.HIGH)
GPIO.cleanup()