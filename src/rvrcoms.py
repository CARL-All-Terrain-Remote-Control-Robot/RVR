#connect/initialize with RVR
#access compass/accel/gyro data
#send movement commands
#change colors


import asyncio
import sys
import os
from carlraspirvr import vprint

sys.path.insert(1,"../include/sphero-sdk-raspberrypi-python")
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import RvrLedGroups

colorDict = {
    "red": [0xff, 0, 0],
    "green": [0, 0xff, 0],
    "blue": [0, 0, 0xff],
    "orange": [0xff, 0xb0, 0],
    "off": [0x00, 0x00. 0x00]
}

class RVRCommunication:

    def __init__(self, loop, printer):
        self.loop = loop
        self.rvr = SpheroRvrAsync(
            dal=SerialAsyncDal(self.loop)
        )


    async def activate(self):
        await self.rvr.wake()
        vprint("")
        await asyncio.sleep(2)
        await self.rvr.reset_yaw()
        self.led_code = "TURNON"

    async def set_color(self, led_code):
        self.led_code = led_code
        self.loop.create_task(change_color())

    #TURNON orange device turned on
    #NETERR red error: no connection to network
    #DEVERR flash orange error: connection to device not working
    #READY green device ready to drive and record
    #RECORD flashing blue recording
    #OFF turn lights off
    """Sets a new color command based on led_code. Create this as a task"""
    """"""
    """loop.create_task(change_color())"""
    async def change_color(self):
        if self.led_code == "TURNON":
            await set_all_leds("orange")
        elif self.led_code == "NETERR" :
            await set_all_leds("red")
        elif self.led_code == "DEVERR":
            await flash_lights("orange")
        elif self.led_code == "READY":
            await set_all_leds("orange")
        elif self.led_code == "RECORD":
            await flash_lights("blue")
        else:
            await set_all_leds("off")

    """flashes lights when flashing = True."""
    async def flash_lights(self,color):
        lights_on = True
        while self.led_code == "RECORD":
            lights_on = not lights_on
            if lights_on:
                await set_all_leds(color)
            else:
                await set_all_leds("off")
            await asyncio.sleep(0.25)

    """Sets all leds on rvr to given color"""
    async def set_all_leds(self, color):
        rgb_val=colorDict[color]
        await self.rvr.set_all_leds(
            led_group = RvrLedGroups.all_lights.value,
            led_brightness_values = [val for x in range(10) for val in colorDict[rgb_val]]
        )
        await asycio.sleep(0.01)






    #if new_code != self.led_code:
    #self.led_code = new_code
    #set_color()


    """motor values can be from 0-255"""
    #Using WASD, W is full forward, S is full backward,
    #A or D are stop and spin, A and D or W aand S do nothing
    #a horiz direction and vert direction do one full and one half
    #possible vals are -1,0,1
    async def moveMotors(self, horiz_val, vert_val, wait_time):
        left_speed = 0
        right_speed = 0

        if vert_val != 0:

        elsif horiz_val != 0:

        else:


        if wait_time != 0:
            await asyncio.sleep(wait_time)

    async def deactivate(self):
        await asyncio.sleep(1)
        await self.rvr.close()
