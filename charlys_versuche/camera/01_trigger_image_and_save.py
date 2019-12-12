# first try to trigger an image and save it
# wait for 10 seconds before triggering the next one

import sys
import gi
import time
import numpy as np
import cv2
import TIS

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")

from gi.repository import Tcam, Gst


# class where images are stored in
class image_data:
    # initialize data storage
    def __init__(self, receive):
        self.images = [] # list to save all images
        self.busy = False
        self.receive = receive

    # add an image to the list
    def add_image(self, new_img):
        self.busy = True
        self.images = np.append(new_img)
        self.busy = False

    # display all images taken so far
    def show_images(self):
        self.busy = True
        if len(self.images) == 0:
            print("No images stored")
            return
        namedWindow("Display Window", WINDOW_AUTOSIZE)
        i = 0
        print("to save the image, press 's' \nTo see the next image, press 'n'\nTo stop, press ESC\n")
        for im in self.images:
            cv2.imshow("Display Window", im)
            k = cv2.waitKey(0)
            if k == ord('s'): # wait for 's' key to save the image
                save_im = "image_" + i + ".jpg"
                cv2.imwrite(save_im, im)
                i += 1
            elif k == 27: # wait for ESC key to exit
                cv2.destroyAllWindows()
            else: # open next image
                continue
        cv2.destroyAllWindows()
        self.busy = False


# callback function to check whether image can be taken or not
def on_new_image(cam, imdata):
    if imdata.busy is True:
        return
    imdata.busy = True
    imdata.receive = True
    imdata.add_image(cam.Get_image())
    imdata.busy = False


# function to set camera parameters to enable best performance
def setup_camera(cam):
    # set up for colour camera
    cam.Set_Property("Whitebalance Auto", False)
    cam.Set_Property("Whitebalance Red", 64)
    cam.Set_Property("Whitebalance Green", 50)
    cam.Set_Property("Whitebalance Blue", 64)

    # Check, whether gain auto is enabled. If so, disable it.
    if cam.Get_Property("Gain Auto").value:
        camera.Set_Property("Gain Auto", False)
        print("Gain Auto now : %s " % camera.Get_Property("Gain Auto").value)
    camera.Set_Property("Gain", 0)
    # Now do the same with exposure. Disable automatic if it was enabled
    # then set an exposure time.
    if camera.Get_Property("Exposure Auto").value:
        camera.Set_Property("Exposure Auto", False)
        print("Exposure Auto now : %s " % camera.Get_Property("Exposure Auto").value)
    camera.Set_Property("Exposure", 24000)
    return True


# function to trigger an image
## param num: how many pictures should be taken
## param cam: camera which takes the images
## return: True if all pictures were taken - False if something went wrong
def trigger_image(cam, num, imData):
    print("start trigger image")
    # don't start pipeline if imData is still busy
    while imData.busy:
        continue
    cam.Set_Property("Trigger Mode", False)
    # start pipeline
    print("start pipeline")
    cam.Start_pipeline()
    time.sleep(2)
    print("pipeline started, setting properties")
    # start trigger mode
    cam.Set_Property("Trigger Mode", True)
    time.sleep(200)
    print("properties are set")
    key = 0
    try:
        cam.Set_Property("Software Trigger", 1)
        print("Software Trigger on")
        while key != 27 and num > 0: # Abbruchbedingung --> press ESC

            # wait for new image
            print("wait for new image")
            tries = 10
            new_img = cam.Get_image()
            while imData.receive is False and tries > 0:
                time.sleep(0.1)
                tries -= 1
            # If new image is there to handle
            if imData.receive:
                imData.receive = False
                num -= 1
            else:
                    print("no image received")
            key = cv2.waitKey(10)
    except KeyboardInterrupt:
        cam.Stop_pipeline()
        return False
    cam.Stop_pipeline()
    return True


if __name__=="__main__":
    camera = TIS.TIS("21910036", 640, 480, 15, True)  # serial, width, height, frame, colour
    imData = image_data(False)
    camera.Set_Image_Callback(on_new_image, imData)
    if setup_camera(camera):
        print("camera is set up")
    b = trigger_image(camera, 10, imData)
    if b:
        print("all images were taken")
    imData.show_images()