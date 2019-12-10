# first try to trigger an image and save it
# wait for 10 seconds before triggering the next one

import sys
import gi
import time

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")

from gi.repository import Tcam, Gst

# function to trigger an image
def trigger_image():
    Gst.init(sys.argv) # init gstreamer
    serial = None
    pipeline = Gst.parse_launch("tcambin name=source"
                                "! video/x-raw, format=BGRx, width=640, height=480, framerate=30/1"
                                "! videoconvert"
                                "! ximagesink"
                                "! filesink name=fsink")
    source = pipeline.get_by_name("source")

    # serial is defined, thus make the source open that device
    if serial is not None:
        source.set_property("serial", serial)

    # save image location
    file_location = "~/"

    # FIXME test camera for 2 seconds before switching to trigger mode
    pipeline.set_state(Gst.State.PLAYING)
    time.sleep(2)

    # activate trigger mode
    source.set_tcam_property("Trigger Mode", True)
    # trigger image
    ret = source.set_tcam_property("Software Trigger", True)
    print(ret)
    time.sleep(10)
    # deactivate trigger mode
    source.set_tcam_property("Trigger Mode", False)

    # stop pipeline and free all resources wait 30 seconds
    pipeline.set_state(Gst.State.NULL)

if __name__=="__main__":

    trigger_image()
