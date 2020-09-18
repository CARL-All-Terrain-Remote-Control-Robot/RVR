#Main class for program
#initialize all classes and start control loop
#main computation
import asyncio
import sys
#from datetime import datetime


"""Create verbose function. Use like so: vprint("1st arg", obj2(), 3)"""
verboseMatch = []
for x in ["-V", "-v", "-verbose"]:
    verboseMatch.append(x in sys.argv)


"""fix!!! doesnt pprint first word"""
if any(verboseMatch):
    print("Verbose on")
    def vprint(self, *args):
        for arg in args:
            print(arg, end =" ")
        print()
        #print(f"({datetime.now()})")
else:
    vprint = lambda *a: None


"""import other Carl RVR files"""
#from rvrcoms import RVRCommunication
#import filemanagement
#import gps
#import networking
#import camera


try:
    loop = asyncio.get_running_loop()

except RuntimeError:
    loop = asyncio.new_event_loop()


async def main():
    vprint("hey", 1, "bro")


if __name__ == "__main__":
    try:
        #connect to RVR and
        #await asyncio.gather(connect to GPS connect to camera)
        #await start connection as server with laptop
        print("hello print")
        vprint("hello vprint", 1, "yo")
        """run control loop"""
        #loop.create_task(main())
        #loop.run_forever()

    except KeyboardInterrupt:
        print("\nKeyboard KeyboardInterrupt")

    finally:
        if loop.is_running():
            loop.close()
