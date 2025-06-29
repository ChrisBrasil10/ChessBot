"""Implements a HD44780 character LCD connected via PCF8574 on I2C."""
#Source: https://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming

import time

import smbus

from lcd_api import LcdApi

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27

# Defines shifts or masks for the various LCD line attached to the PCF8574

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4

class I2cLcd(LcdApi):
    """Implements a HD44780 character LCD connected via PCF8574 on I2C."""

    def __init__(self, port, i2c_addr, num_lines, num_columns):
        self.port = port
        self.i2c_addr = i2c_addr
        self.bus = smbus.SMBus(port)
        self.bus.write_byte(self.i2c_addr, 0)
        time.sleep(0.020)    # Allow LCD time to powerup
        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.005)   # need to delay at least 4.1 msec
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        time.sleep(0.001)
        # Put LCD into 4 bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        time.sleep(0.001)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        """Writes an initialization nibble to the LCD.
        This particular function is only used during initialization.
        """
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)

    def hal_backlight_on(self):
        """Allows the hal layer to turn the backlight on."""
        self.bus.write_byte(self.i2c_addr, 1 << SHIFT_BACKLIGHT)

    def hal_backlight_off(self):
        """Allows the hal layer to turn the backlight off."""
        self.bus.write_byte(self.i2c_addr, 0)

    def hal_sleep_us(self, usecs):
        """Sleep for some time (given in microseconds)."""
        time.sleep(usecs / 1000000)

    def hal_write_command(self, cmd):
        """Writes a command to the LCD.
        Data is latched on the falling edge of E.
        """
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
        if cmd <= 3:
            # The home and clear commands require a worst
            # case delay of 4.1 msec
            time.sleep(0.005)

    def hal_write_data(self, data):
        """Write data to the LCD."""
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        self.bus.write_byte(self.i2c_addr, byte | MASK_E)
        self.bus.write_byte(self.i2c_addr, byte)
