#add ability to create file for csv file and another for images
#create .csv file
#append to .csv file
#create error file upon error
import asyncio
import sys
import os
import time
from carlraspirvr import vprint


"""Change depending on used sensors"""
header = [
    "time",
    "imu",
    "accelerometer",
    "locator",
    "velocity"
]

class FileManager():

    def __init__(self,file_location=os.getcwd()):
        try:
            self.my_time = time.localtime(time.time())

            self.time_string = f"{self.my_time.tm_mon}_{self.my_time.tm_mday}_{self.my_time.tm_year}_{self.my_time.tm_hour}:{self.my_time.tm_min}:{self.my_time.tm_sec}"

            self.file_location = file_location + "/"

            self.new_dir_name = "collected_data_" + self.time_string
            self.image_dir_name = "images"

            self.new_dir = os.path.join(self.file_location, self.new_dir_name)
            self.image_dir = os.path.join(self.new_dir, self.image_dir_name)

            #create new directories
            os.mkdir(self.new_dir)
            os.mkdir(self.image_dir)
            #create csv file to add information to
            new_file = os.path.join(self.new_dir ,"data.csv")
            self.f = open(new_file, "a+")

            for title in header:
                self.f.write(title)
                if title != header[len(header)-1]:
                    self.f.write(",")
            self.f.write("\n")
            vprint("Files Created")

        except IOError as e:
            vprint("IO error")

        except Exception as e:
            vprint(e)

    """Call at end to close file"""
    def close_file(self):
        self.f.close()

    """given dict with header as key and value is its respective value"""
    """Keys must have same names as header values"""
    """all values must be strings"""
    def write_to_file(self, data):
        for title in header:
            if title in data:
                self.f.write(data[title])
            else:
                self.f.write("NONE")
            if title != header[len(header)-1]:
                self.f.write(",")
        self.f.write("\n")


    """saves an image to file"""
    def create_image(self, time_string):
        image_name = time_string + ".jpg"
        image_file = os.path.join(self.image_dir,image_name)
        file = open(image_file, "wb")
        return file
