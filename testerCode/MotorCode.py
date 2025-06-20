import RPi.GPIO as GPIO
import time

t = 0.001

out1 = 13
out2 = 11
out3 = 15
out4 = 12

i = 0
positive = 0
negative = 0
y = 0

low = GPIO.LOW
high = GPIO.HIGH

GPIO.setmode(GPIO.BOARD)

GPIO.setup(out1, GPIO.OUT)
GPIO.setup(out2, GPIO.OUT)
GPIO.setup(out3, GPIO.OUT)
GPIO.setup(out4, GPIO.OUT)

def pinout (pin, output):
    GPIO.output(pin, output)

def allpinsSet(outputA, outputB, outputC, outputD):
    pinout(out1, outputA)
    pinout(out2, outputB)
    pinout(out3, outputC)
    pinout(out4, outputD)

print("First calibrate by giving some +ve and -ve values")

try:
    while True:
        pinout(out1, low)
        pinout(out2, low)
        pinout(out3, low)
        pinout(out4, high)
        
        x = int(input())
        
        if x > 0:
            for y in range(x, 0, -1):
                if negative == 1:
                    if i == 7:
                        i = 0
                    else:
                        i = i+1
                    y = y+2
                    negative = 0
                positive = 1
                
                if i == 0:
                    allpinsSet(high, low, low, low)
                    time.sleep(t)
                elif i == 1:
                    allpinsSet(high, high, low, low)
                    time.sleep(t)
                elif i == 2:
                    allpinsSet(low, high, low, low)
                    time.sleep(t)
                elif i == 3:
                    allpinsSet(low, high, high, low)
                    time.sleep(t)
                elif i == 4:
                    allpinsSet(low, low, high, low)
                    time.sleep(t)
                elif i == 5:
                    allpinsSet(low, low, high, high)
                    time.sleep(t)
                elif i == 6:
                    allpinsSet(low, low, low, high)
                    time.sleep(t)
                elif i == 7:
                    allpinsSet(high, low, low, high)
                    time.sleep(t)
                    
                if i == 7:
                    i = 0
                    continue
                i = i+1
                
                
        if x < 0:
            
            x = x* -1
            
            for y in range(x, 0, -1):
                if positive==1:
                    if i == 0:
                        i = 7
                    else:
                        i = i-1
                    y = y+3
                    positive = 0
                negative = 1
                
                if i == 0:
                    allpinsSet(high, low, low, low)
                    time.sleep(t)
                elif i == 1:
                    allpinsSet(high, high, low, low)
                    time.sleep(t)
                elif i == 2:
                    allpinsSet(low, high, low, low)
                    time.sleep(t)
                elif i == 3:
                    allpinsSet(low, high, high, low)
                    time.sleep(t)
                elif i == 4:
                    allpinsSet(low, low, high, low)
                    time.sleep(t)
                elif i == 5:
                    allpinsSet(low, low, high, high)
                    time.sleep(t)
                elif i == 6:
                    allpinsSet(low, low, low, high)
                    time.sleep(t)
                elif i == 7:
                    allpinsSet(high, low, low, high)
                    time.sleep(t)
                    
                if i == 0:
                    i = 7
                    continue
                i = i-1
except KeyboardInterrupt:
    GPIO.cleanup()
                    
                