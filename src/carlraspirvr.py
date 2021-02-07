import asyncio
import sys
import os
import time
import json

from vprint import vprint
from rvrcoms import RVRCommunication

from sphero_sdk import RvrLedGroups
from sphero_sdk import Colors
#from helper_keyboard_input import KeyboardHelper
import rvrNetwork
import filemanagement
#import gps

import camera
#from datetime import datetime

sys.path.append(os.path.dirname(__file__))
sys.path.insert(1,"../include/sphero-sdk-raspberrypi-python/projects/keyboard_control")

class Controller():

    def __init__(self, file_path=None):
        self.make_loop()
        self.file_path = file_path

    def initialize(self):
        self.myRVR = RVRCommunication(self.loop)
        self.test_val = "heyo"
        self.network = rvrNetwork.NetworkServer(self.myRVR)


        if file_path:
           self.fman = filemanagement.FileManager(self.file_path)
        else:
            self.fman = filemanagement.FileManager()

        self.cam = camera.Camera(self.fman, myRVR = self.myRVR)
        vprint("initialized sensors")

        """Create a group of tasks to run asyncronously"""
        """activate sensors"""
        #start_up_rvr = asyncio.gather(myRVR.activate(), asyncio.sleep(5))
        #start_up_sensors = asyncio.gather(await cam.activate())
        self.loop.run_until_complete(self.myRVR.activate())
        self.loop.run_until_complete(asyncio.sleep(3))
        self.loop.run_until_complete(self.cam.activate())
        self.loop.run_until_complete(asyncio.sleep(3))
        vprint("activated sensors")

        self.network.start_servers()
        vprint("server started")
        self.header = self.loop.run_until_complete(self.network.get_init_tcp())

        vprint(self.header)
        self.control_loop = True
        self.drive = self.loop.create_task(self.drive_loop())
        self.myRVR.set_color("READY")
        while(self.control_loop):
            measurements = self.make_measurements()
            data = json.dumps(measurements)
            self.network.udp_send_data  = data
            self.loop.run_until_complete(self.myRVR.update_battery_state())
            self.loop.run_until_complete(asyncio.sleep(.5))
        """"If something wrong exit"""
        #try:
        #   start network
        #except:
        #   loop.run_until_complete(asyncio.gather(rvr.set_color("NETERR"), asyncio.sleep(10)))

        #    while(True):
        #        bat = myRVR.get_battery_state()
        #        imu = myRVR.get_imu()
        #        if bat != None and imu != None:
        #            print(f"battery state is {bat}")
        #            print(f"Imu stuff is {imu}")

        #loop.run_until_complete(
    #def control_loop(self):
    #    vprint()
    async def drive_loop(self):
        while self.control_loop:
            direction = self.network.get_direction()
            vprint("directipn: ", direction)
            await self.myRVR.moveMotors(direction)


    def  make_loop(self):
        try:
            self.loop = asyncio.get_running_loop()

        except RuntimeError:
            vprint("Creating new event loop")
            self.loop = asyncio.new_event_loop()

        except Exception as e:
            vprint(e)

    def get_command(self):
        command = self.network.udp_rcv_data
        self.udp_read = True
        vprint("recieved command "+ command)
        return command

    def make_measurements(self):
        vprint("making measurements")

        t = time.localtime(time.time())
        time_string = f"{t.tm_mon}_{t.tm_mday}_{t.tm_year}_{t.tm_hour}:{t.tm_min}:{t.tm_sec}"
        sensor_dict = {
            "time": time_string,
            "gyro":f"{self.myRVR.get_gyroscope()}",    #this needs to be changed
            "accelerometer":f"{self.myRVR.get_accelerometer()}",
            "locator":f"{self.myRVR.get_locator()}",
            "velocity":f"{self.myRVR.get_velocity()}",
            "battery":f"{self.myRVR.get_battery_state()}"
        }
        self.fman.write_to_file(sensor_dict)
        self.cam.take_image(time_string)
        keys = list(sensor_dict.keys())
        send_sensor = {}
        for item in self.header:
            if item in keys:
                send_sensor[item]=sensor_dict[item]
        return  send_sensor

    def shut_down(self):
        self.control_loop = False
        vprint("deactivating rvr")
        self.loop.run_until_complete(self.myRVR.deactivate())
        if self.network:
            vprint("deactivating Network")
            self.network.stop_networks()

        if self.loop.is_running():
            vprint("deactivating loop")
            self.loop.close()

        try:
            vprint("deactivating filemanager")
            self.fman.close_file()
        except NameError as e:
            vprint(e)
        except Exception as e:
            vprint("Error in activation. Exception: ",e)
        finally:
            vprint("All closed")

c = None
"""Starts whole process"""
if __name__ == "__main__":
    pathMatch = []
    for x in sys.argv:
        pathMatch.append(x.lower() in ["-p", "--path"])
    c = None
    file_path = None
    if any(pathMatch):
        file_path = sys.argv[pathMatch.index(True) + 1]
        if not os.path.exists(file_path):
            vprint(f"Invalid path: {file_path}")
            exit()
        else:
            vprint(f"saving files to {file_path}")



    try:
        if file_path:
            c = Controller(file_path)
        else:
            c = Controller()
        c.initialize()
        vprint(c.test_val)

    except KeyboardInterrupt:
        print("\nKeyboard KeyboardInterrupt")

    except Exception as e:
        vprint("something went wrong", e)

    finally:
        try:
            vprint("Shutting Down")
            c.shut_down()
        except Exception as e:
            vprint("c not created", e)
        finally:
            exit(1)
