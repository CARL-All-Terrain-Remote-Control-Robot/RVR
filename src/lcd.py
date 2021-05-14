#!/usr/bin/python
#refrence from ...
#https://www.mbtechworks.com/projects/drive-an-lcd-16x2-display-with-raspberry-pi.html 


import RPi.GPIO as GPIO
import time

class LCD():
    def __init__(self):
        # GPIO to LCD mapping
        self.LCD_RS = 16 # Pi pin 26
        self.LCD_E = 18 # Pi pin 24
        self.LCD_D4 = 31 # Pi pin 22
        self.LCD_D5 = 33 # Pi pin 18
        self.LCD_D6 = 35 # Pi pin 16
        self.LCD_D7 = 37 # Pi pin 12

        # Device constants
        self.LCD_CHR = True # Character mode
        self.LCD_CMD = False # Command mode
        self.LCD_CHARS = 16 # Characters per line (16 max)
        self.LCD_LINE_1 = 0x80 # LCD memory location for 1st line
        self.LCD_LINE_2 = 0xC0 # LCD memory location 2nd line

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) # Use BCM GPIO numbers
        GPIO.setup(self.LCD_E, GPIO.OUT) # Set GPIO's to output mode
        GPIO.setup(self.LCD_RS, GPIO.OUT)
        GPIO.setup(self.LCD_D4, GPIO.OUT)
        GPIO.setup(self.LCD_D5, GPIO.OUT)
        GPIO.setup(self.LCD_D6, GPIO.OUT)
        GPIO.setup(self.LCD_D7, GPIO.OUT)

        # Loop - send text and sleep 3 seconds between texts
        # Change text to anything you wish, but must be 16 characters or less
        self.lcd_init()

        self.write("init","init")


    # End of main program code
    def write(self, line1, line2):
        self.lcd_text(line1, self.LCD_LINE_1)
        self.lcd_text(line2, self.LCD_LINE_2)

    # Initialize and clear display
    def lcd_init(self):
        self.lcd_write(0x33,self.LCD_CMD) # Initialize
        self.lcd_write(0x32,self.LCD_CMD) # Set to 4-bit mode
        self.lcd_write(0x06,self.LCD_CMD) # Cursor move direction
        self.lcd_write(0x0C,self.LCD_CMD) # Turn cursor off
        self.lcd_write(0x28,self.LCD_CMD) # 2 line display
        self.lcd_write(0x01,self.LCD_CMD) # Clear display
        time.sleep(0.0005) # Delay to allow commands to process

    def lcd_write(self, bits, mode):
        # High bits
        GPIO.output(self.LCD_RS, mode) # RS

        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        time.sleep(0.0005)
        GPIO.output(self.LCD_E, True)
        time.sleep(0.0005)
        GPIO.output(self.LCD_E, False)
        time.sleep(0.0005)

    def lcd_text(self, message,line):
    # Send text to display
        message = message.ljust(self.LCD_CHARS," ")

        self.lcd_write(line, self.LCD_CMD)

        for i in range(self.LCD_CHARS):
            self.lcd_write(ord(message[i]),self.LCD_CHR)

    def shut_down(self):
        self.lcd_write(0x01, self.LCD_CMD)
        self.lcd_text("Good night",self.LCD_LINE_1)
        self.lcd_text("Sweet prince",self.LCD_LINE_2)
        GPIO.cleanup()

if __name__ == "__main__":
    import socket
    
    l = LCD()
    
    l.write("IP address","please wait")
    # I thought there would be a better way to do this but I could not find one
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        address = s.getsockname()[0]
        print("Local IP address: ", address)
        l.write("IP address",address)
    except:
        l.write("Error while", "searching IP")
