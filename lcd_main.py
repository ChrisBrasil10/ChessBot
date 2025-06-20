"""Implements user input to display on lcd"""
#Source: https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming

from lcd_api import LcdApi
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#input: list with 2 string as values, printes the message and clears the message on lcd
def printMessage(messageList):
    lcd.clear()
    lcd.putstr(messageList[0])
    lcd.move_to(0, 1)
    lcd.putstr(messageList[1])