# Imports the monkeyrunner modules used by this program
print("importing modules...")
print("importing os modules...")
import os
print("importing sys modules...")
import sys
print("importing time modules...")
from time import sleep
print("importing java.lang modules...")
import java.lang
print("importing opencv modules...")
sys.path.append('/D:/Projects/mrTest/opencv-2413.jar')
sys.path.append('/D:/Projects/mrTest/Imshow.jar')
from org.opencv.core import Core as core
from org.opencv.core import CvType, Point, Scalar
from org.opencv.imgproc import Imgproc as cv2
from org.opencv.highgui import Highgui as hg
from org.opencv.core import Mat
from com.atul.JavaOpenCV import Imshow

java.lang.System.loadLibrary('/D:/Projects/mrTest/opencv_java2413')
print("imports done!")



# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
print "Start Connction to Phone"
device = MonkeyRunner.waitForConnection()
print "Connected to Phone"
device.wake()

cnt = 0
fn = "d:\\"
while 1:
    print "Start take snapshot for count:" + cnt
    screenShot = device.takeSnapshot()
    print "End take snapshot for count:" + cnt
    # Writes the screenshot to a file
    fn = "d:\\s" + cnt + ".jpg"
    print "Start write to file :" + fn
    result.writeToFile(fn,'jpg')
    print "Ended write to file"
    print "Start to Sleep 5 secs"
    MonkeyRunner.sleep(5)
