#initialize camera
#take image
#place image into correct file
from carlraspirvr import vprint
import asyncio
import picamera

class Camera():
    def __init__(self, fileManager, image_size=(320, 240), framerate = 30, resolution = (1024, 768)):
        try:
            self.camera = picamera.PiCamera()
            self.camera.resolution = resolution
            self.camera.framerate = framerate
            self.image_size = image_size
            self.fileManager = fileManager

        except Exception as e:
            vprint("something wrong in camera init")
            vprint(e)

    async def activate(self, const_exposure=False):
        self.camera.start_preview()
        vprint("activating cam")
        await asyncio.sleep(2)
        if const_exposure:
            self.camera.shutter_speed = self.camera.exposure_speed
            self.camera.exposure_mode = "off"
            g = self.camera.awb_gains
            self.camera.awb_mode = "off"
            self.camera.awb_gains = g

    def take_image(self, time_string):
        vprint("Taking image")
        file = self.fileManager.create_image(time_string)
        self.camera.capture(file, resize=self.image_size)
        file.close()
