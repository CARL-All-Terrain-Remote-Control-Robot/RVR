import asyncio
import sys
import os
import time
#from datetime import datetime
sys.path.append(os.path.dirname(__file__))
sys.path.insert(1,"../include/sphero-sdk-raspberrypi-python/projects/keyboard_control")

if __name__== "__main__":
    verboseMatch = []
    helpMatch = []
    pathMatch = []

    for x in sys.argv:
        verboseMatch.append(x.lower() in ["-v", "--verbose"])
        helpMatch.append(x.lower() in ["-h", "--help"])
        pathMatch.append(x.lower() in ["-p", "--path"])

    """Create help menu"""
    if any(helpMatch):
        print("use \"-v or --verbose\" for verbose\nuse \"-p or --path\" followed by a valid path to save data to that file")

    if any(pathMatch):
        file_path = sys.argv[pathMatch.index(True) + 1]
        if not os.path.exists(file_path):
            vprint(f"Invalid path: {file_path}")
            exit()
        else:
            vprint(f"saving files to {file_path}")

"""Create verbose function. Essentially just a print with a toggle"""
if any(verboseMatch):
    vprint = print
else:
    vprint = lambda *a, **k: None


class Controller():

    def __init__(self, loop):
        self.loop = loop
        self.myRVR = RVRCommunication(self.loop)
        self.network = NetworkServer(self.myRVR)

        try:
           file_path
           fman = filemanagement.FileManager(file_path)
        except NameError:
            fman = filemanagement.FileManager()

        cam = camera.Camera(fman, myRVR = myRVR)
        vprint("initialized sensors")

        """Create a group of tasks to run asyncronously"""
        """activate sensors"""
        #start_up_rvr = asyncio.gather(myRVR.activate(), asyncio.sleep(5))
        #start_up_sensors = asyncio.gather(await cam.activate())

        """If something wrong exit"""
        #loop.run_until_complete(start_up_rvr)

        loop.run_until_complete(myRVR.activate())
        loop.run_until_complete(asyncio.sleep(3))
        loop.run_until_complete(cam.activate())
        loop.run_until_complete(asyncio.sleep(3))
        vprint("activated sensors")

        network.start_servers()
        vprint("server started")

        control_loop = True
        while(control_loop):
            make_measurements()

            loop.run_until_complete(asyncio.sleep(5))
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
    def get_command(self):


    async def drive(self):
        while key_helper.key_code not in driving_keys:
            print('Drive with key code: ', str(key_helper.key_code))
            await asyncio.sleep(0.05)
        print('Drive with key code: ', str(key_helper.key_code))
        if key_helper.key_code == 113:
            break_loop = True
        key_helper.key_code = -1


    def make_measurements(self):
        global myRVR
        global fman
        global cam
        vprint("making measurements")
        t = time.localtime(time.time())
        time_string = f"{t.tm_mon}_{t.tm_mday}_{t.tm_year}_{t.tm_hour}:{t.tm_min}:{t.tm_sec}"
        sensor_dict = {
            "time": time_string,
            "imu":f"{myRVR.get_imu()}",
            "accelerometer":f"{myRVR.get_accelerometer()}",
            "locator":f"{myRVR.get_locator()}",
            "velocity":f"{myRVR.get_velocity()}"
        }
        fman.write_to_file(sensor_dict)
        cam.take_image(time_string)


"""Starts whole process"""
if __name__ == "__main__":
    """import other Carl RVR files"""
    from rvrcoms import RVRCommunication
    from sphero_sdk import RvrLedGroups
    from sphero_sdk import Colors
    from helper_keyboard_input import KeyboardHelper
    import filemanagement
    #import gps
    import networking
    import camera

    try:
        try:
            loop = asyncio.get_running_loop()

        except RuntimeError:
            vprint("Creating new event loop")
            loop = asyncio.new_event_loop()

        c = Controller(loop)

    except KeyboardInterrupt:
        print("\nKeyboard KeyboardInterrupt")
        #filemamager.close_file

    finally:
        loop.run_until_complete(myRVR.deactivate())
        if network:
            network.udp_close = network.tcp_close = True
        if loop.is_running():
            loop.close()
        try:
            fman.close_file()
        except NameError as e:
            vprint(e)
        finally:
            #key_helper.end_get_key_continuous()
            vprint("All closed")
            exit(1)
