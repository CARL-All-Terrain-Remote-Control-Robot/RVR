#connect/initialize with RVR
#access compass/accel/gyro data
#send movement commands
#change colors


import asyncio
import sys
import os
from vprint import vprint

sys.path.insert(1,"../include/sphero-sdk-raspberrypi-python")
from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from sphero_sdk import RvrLedGroups
from sphero_sdk import BatteryVoltageStatesEnum as VoltageStates
from sphero_sdk import RvrStreamingServices

colorDict = {
    "red": [0xff, 0, 0],
    "green": [0, 0xff, 0],
    "blue": [0, 0, 0xff],
    "orange": [0xff, 0xb0, 0],
    "off": [0x00, 0x00, 0x00]
}

class RVRCommunication():

    def __init__(self, loop):
        self.loop = loop
        self.rvr = SpheroRvrAsync(
            dal=SerialAsyncDal(self.loop)
        )
        vprint("RVR initialized")


    async def activate(self):
        try:
            await self.rvr.wake()
            vprint("RVR wake successful")
            await asyncio.sleep(2)
            await self.rvr.reset_yaw()
            self.led_code = "TURNON"
            await self.change_color()
            await self.start_data_handling()
            vprint("IMU start successful")
            self.light_task = None
            self.speed_limit = 255
            self.battery_percentage = 0
            self.gyroscope_data = None
            self.accelerometer_data = None
            self.locator_data = None
            self.velocity_data = None

        except Exception as e:
            vprint("Error in activation. Exception: ",e)


    def set_color(self, led_code):
        vprint("setting color")
        vprint(led_code)
        self.led_code = led_code
        if not self.light_task:
            self.light_task = self.loop.create_task(self.change_color())
        else:
            self.light_task.cancel()
            self.light_task = self.loop.create_task(self.change_color())


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
        vprint("Changing color")
        if self.led_code == "TURNON":
            await self.set_all_leds("orange")
        elif self.led_code == "NETERR" :
            await self.set_all_leds("red")
        elif self.led_code == "DEVERR":
            await self.flash_lights("orange")
        elif self.led_code == "READY":
            await self.set_all_leds("green")
        elif self.led_code == "RECORD":
            await self.flash_lights("blue")
        else:
            await self.set_all_leds("off")


    """flashes lights when flashing = True."""
    async def flash_lights(self,color):
        vprint("Flashing Lights")
        lights_on = True
        while self.led_code == "RECORD":
            lights_on = not lights_on
            if lights_on:
                await self.set_all_leds(color)
            else:
                await self.set_all_leds("off")
            await asyncio.sleep(0.25)
        vprint("Stopping flashing Lights")


    """Sets all leds on rvr to given color"""
    async def set_all_leds(self, color):
        vprint(f"setting all leds to {color}")
        rgb_val=colorDict[color]
        await self.rvr.set_all_leds(
            led_group = RvrLedGroups.all_lights.value,
            led_brightness_values = [color for x in range(10) for color in rgb_val]
        )
        await asyncio.sleep(0.01)


    """motor values can be from 0-255"""
    #Using WASD, W is full forward, S is full backward,
    #A or D are stop and spin, A and D or W aand S do nothing
    #a horiz direction and vert direction do one full and one half
    #possible vals are -1,0,1 forward and right are positive
    async def moveMotors(self, direction, speed=0.5, wait_time=.05):
        if direction == 1:
            await self.rvr.raw_motors(1, int(self.speed_limit*speed), 1, int(self.speed_limit*speed))
        elif direction == 2:
            await self.rvr.raw_motors(2, int(self.speed_limit*speed), 2, int(self.speed_limit*speed))
        elif direction == 3:
            await self.rvr.raw_motors(1, int(self.speed_limit*speed), 1, int(self.speed_limit*speed/2))
        elif direction == 4:
            await self.rvr.raw_motors(1, int(self.speed_limit*speed/2), 1, int(self.speed_limit*speed))
        elif direction == 5:
            await self.rvr.raw_motors(2, int(self.speed_limit*speed), 2, int(self.speed_limit*speed/2))
        elif direction == 6:
            await self.rvr.raw_motors(2, int(self.speed_limit*speed/2), 2, int(self.speed_limit*speed))
        elif direction == 7:
            await self.rvr.raw_motors(1, int(self.speed_limit*speed), 2, int(self.speed_limit*speed))
        elif direction == 8:
            await self.rvr.raw_motors(2, int(self.speed_limit*speed), 1, int(self.speed_limit*speed))
        else:
            await self.rvr.raw_motors(0, 0, 0, 0)

        if wait_time != 0:
            await asyncio.sleep(wait_time)


    """Updates object's battery state"""
    async def update_battery_state(self):
        self.battery_percentage = await self.rvr.get_battery_percentage()


    def get_battery_state(self):
        return self.battery_percentage

#streaming service configuration for RVR:
#        | Id     | Processor          | Token | Service            | Attributes                 |
#        | ------ | ------------- -----| ----- | ------------------ | -------------------------- |
#        | 0x0003 | Nordic (1)         | 1     | ColorDetection     | R, G, B, Index, Confidence |
#        | 0x000A | Nordic (1)         | 2     | AmbientLight       | Light                      |
#        -----------------------------------------------------------------------------------------
#        | 0x0000 | ST (2)             | 1     | Quaternion         | W, X, Y, Z                 |
#        | 0x0001 | ST (2)             | 1     |                 | Pitch, Roll, Yaw           |
#        | 0x0002 | ST (2)             | 1     | Accelerometer      | X, Y, Z                    |
#        | 0x0004 | ST (2)             | 1     | Gyroscope          | X, Y, Z                    |
#        | 0x0006 | ST (2)             | 2     | Locator            | X, Y                       |
#        | 0x0007 | ST (2)             | 2     | Velocity           | X, Y                       |
#        | 0x0008 | ST (2)             | 2     | Speed              | Speed                      |
#        | 0x000B | ST (2)             | 2     | Encoders           | Left, Right                |
#        -----------------------------------------------------------------------------------------
#        | 0x0009 | Nordic (1), ST (2) | 3     | CoreTime           | TimeUpper, TimeLower       |
#        -----------------------------------------------------------------------------------------
    """Begins handler that streams imu data every 200 ms.Imu handler saves to object variable"""
    async def start_data_handling(self):
        await self.rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.gyroscope,
            handler=self.gyroscope_handler
        )
        await self.rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.accelerometer,
            handler=self.accelerometer_handler
        )
        await self.rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.locator,
            handler=self.locator_handler
        )
        await self.rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.velocity,
            handler=self.velocity_handler
        )
        """!!!maybe change to whatever the rate of data collection is"""

        await self.rvr.sensor_control.start(interval=200)


    async def gyroscope_handler(self, gyroscope_data):
        await self.update_battery_state()
        self.gyroscope_data = gyroscope_data


    def get_gyroscope(self):
        return self.gyroscope_data


    async def accelerometer_handler(self, accelerometer_data):
        self.accelerometer_data = accelerometer_data


    def get_accelerometer(self):
        return self.accelerometer_data


    async def locator_handler(self, locator_data):
        self.locator_data = locator_data


    def get_locator(self):
        return self.locator_data


    async def velocity_handler(self, velocity_data):
        self.velocity_data = velocity_data


    def get_velocity(self):
        return self.velocity_data


    async def deactivate(self):
        vprint("Deactivating")
        self.set_color("OFF")
        await asyncio.sleep(1)
        await self.rvr.sensor_control.stop()
        await self.rvr.sensor_control.clear()
        await asyncio.sleep(1)
        await self.rvr.close()
