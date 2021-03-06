# first try to trigger an image and save it
import gi
import time
import numpy as np
import cv2
import TIS

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")


# class where images are stored in
class image_data:
    # initialize data storage
    def __init__(self, receive):
        self.images = [] # list to save all images
        self.busy = False
        self.receive = receive # has an image been received and not yet worked with?
        self.new_img = [] # save newest image


    # add an image to the list
    def add_image(self, new_img):
        self.busy = True
        self.images.append(new_img)
        print("image appended")
        self.busy = False

    # save all images taken so far
    # remove all images from list  after saving them
    def save_images(self, run, circle):
        self.busy = True
        if len(self.images) == 0:
            print("No images stored")
            return
	# list with number of images
	numImages = [i for i in range(len(self.images))]
        # save images in folder: run/circle/imNumber.tif
	for im, imNumber in zip(self.images, numImages):
            save_im = "~/Documents/images/run" + str(run) + "/circle" + str(circle) + "/"  + "image_" + str(imNumber) + ".tif"
            cv2.imwrite(save_im, im)
        # remove images
        self.images.clear()
        self.busy = False

    # display all images taken so far
    def show_images(self):
        self.busy = True
        if len(self.images) == 0:
            print("no images stored")
            return
        cv2.namedWindow("Display Window", cv2.WINDOW_NORMAL)
        key = 0
        for im in self.images:
            if key != 27:
                cv2.imshow("Display Window", im)
            key = input("To view next image, press 'n'\nTo stop, press ESC: ")
        self.busy = False


# callback function to check whether image can be taken or not
def on_new_image(cam, imdata):
    if imdata.busy is True:
        return
    imdata.busy = True
    imdata.receive = True
    imdata.new_img = cam.Get_image()
    imdata.busy = False


# function to set camera parameters to enable best performance
# returns camera and object in which images are stored during one whole circulation
def setup_camera():
    # define camera
    cam = TIS.TIS("21910036", 640, 480, 15, True) # serial, width, height, frame, colour

    # object in which data is stored during one full rotation
    imData = image_data(False)

    # set callback function
    cam.Set_Image_Callback(on_new_image, imData)


    #### Setting camera parameters
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

    return cam, imData


# function to trigger an image
## param num: how many pictures should be taken
## param cam: camera which takes the images
## return: True if all pictures were taken - False if something went wrong
def trigger_image(cam, num, imData):
    print("setting Trigger Mode")
    cam.Set_Property("Trigger Mode", True)
    time.sleep(20)
    # take all images
    while num != len(imData.images):
		# wait for new image
                cam.Set_Property("Software Trigger", 1)
                tries = 10
                while imData.receive is False and tries > 0:
                	time.sleep(0.1)
                	tries -= 1
                # If new image is there to handle
                if imData.receive is True:
                	imData.add_image(imData.new_img)
                	imData.receive = False
                else:
                	print("no image received")
                	print(len(imData.images))
			return False

    return True



if __name__=="__main__":
    # initialize camera
    #camera = TIS.TIS("21910036", 640, 480, 15, True)  # serial, width, height, frame, colour

    # object in which data is stored during one full rotation
    #imData = image_data(False)

    # set callback function
    #camera.Set_Image_Callback(on_new_image, imData)

    # set up camera
    #if setup_camera(camera):
        #print("camera is set up")

    # trigger images
    #b = trigger_image(camera, 5, imData)  # camera, number of images, where to save them
    #print("saving all images")
    #imData.save_images()
    #print("Platform rotated back to origin")
    #print("Process successful")
