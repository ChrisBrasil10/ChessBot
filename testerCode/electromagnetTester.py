import RPi.GPIO as GPIO
import time

electromagnet_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(electromagnet_pin, GPIO.OUT)

def electromagnet(on):
    output = GPIO.HIGH if on else GPIO.LOW
    GPIO.output(electromagnet_pin, output)



electromagnet(False)

#electromagnet(False
