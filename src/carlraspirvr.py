import asyncio
import sys
import os
import time

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
        self.myRVR = RVRCommunication(self.loop)

        self.network = rvrNetwork.NetworkServer(self.myRVR)


        if file_path:
           self.fman = filemanagement.FileManager(file_path)
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

        control_loop = True
        while(control_loop):
            self.make_measurements()

            self.loop.run_until_complete(asyncio.sleep(5))
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
    def control_loop(self):
        vprint()

    def  make_loop(self):
        try:
            self.loop = asyncio.get_running_loop()

        except RuntimeError:
            vprint("Creating new event loop")
            self.loop = asyncio.new_event_loop()

    def get_command(self):
        vprint()

    def make_measurements(self):
        vprint("making measurements")
        t = time.localtime(time.time())
        time_string = f"{t.tm_mon}_{t.tm_mday}_{t.tm_year}_{t.tm_hour}:{t.tm_min}:{t.tm_sec}"
        sensor_dict = {
            "time": time_string,
            "imu":f"{self.myRVR.get_imu()}",
            "accelerometer":f"{self.myRVR.get_accelerometer()}",
            "locator":f"{self.myRVR.get_locator()}",
            "velocity":f"{self.myRVR.get_velocity()}"
        }
        self.fman.write_to_file(sensor_dict)
        self.cam.take_image(time_string)

    def shut_down(self):
        self.loop.run_until_complete(self.myRVR.deactivate())
        if self.network:
            self.network.udp_close = self.network.tcp_close = True

        if self.loop.is_running():
            self.loop.close()

        try:
            self.fman.close_file()
        except NameError as e:
            vprint(e)
        finally:
            vprint("All closed")


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


    except KeyboardInterrupt:
        print("\nKeyboard KeyboardInterrupt")

    except Exception as e:
        vprint("something went wrong", e)

    finally:
        try:
            c.shut_down()
        except:
            vprint("c not created")
        finally:
            exit(1)
