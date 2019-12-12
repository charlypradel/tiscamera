import cv2
import time
import gi
import sys
from gi.repository import Tcam, Gst
import TIS

class image_Data:
    def __init__(self, newImageReceived, newimage):
        self.newImageReceived = newImageReceived # bool
        self.image = newimage # the new image
        self.busy = False


imageData = image_Data(False, None)

# Callback function for each camera element
def new_image(camera, data):
    if data.busy is True:
        return
    data.busy = True
    data.newImageReceived = True
    data.image = camera.Get_image()
    data.busy = False


# set camera
camera = TIS.TIS("21910036", 640, 480, 15, True) # serial, width, height, frame, colour
camera.Set_Image_Callback(new_image, image_Data)

# set up trigger mode
camera.Set_Property("Trigger Mode", False)
image_Data.busy = True # only one image at a time should be handled

# start pipeline
camera.Start_pipeline()

# start trigger mode
camera.Set_Property("Trigger Mode", True)
time.sleep(2)
image_Data.busy = False

try:
        while lastkey != 27 and error < 5:
                time.sleep(1)
                camera.Set_Property("Software Trigger",1) # Send a software trigger

                # Wait for a new image. Use 10 tries.
                tries = 10
                while imageData.newImageReceived is False and tries > 0:
                        time.sleep(0.1)
                        tries -= 1

                # Check, whether there is a new image and handle it.
                if imageData.newImageReceived is True:
                        imageData.newImageReceived = False
                        cv2.imshow('Window', imageData.image)
                else:
                        print("No image received")

                lastkey = cv2.waitKey(10)

except KeyboardInterrupt:
        cv2.destroyWindow('Window')

# Stop the pipeline and clean ip
print(imageData.busy, imageData.image, imageData.newImageReceived)
camera.Stop_pipeline()
cv2.destroyAllWindows()
print('Program ends')