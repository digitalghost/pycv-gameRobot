import subprocess
import time

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice



# Connects to the current device, returning a MonkeyDevice object
print "Start Connction to Phone"
device = MonkeyRunner.waitForConnection()
print "Connected to Phone"
device.wake()

pWidth = device.getProperty("display.width")
pHeight = device.getProperty("display.height")
print "device width:" + str(pWidth) + ", Height:" + str(pHeight) + ", Density:" + str(device.getProperty("display.density"))

cnt = 0
fn = "d:\\"
while 1:
    startTick = time.time()
    print "Start take snapshot for count:" + str(cnt)
    screenShot = device.takeSnapshot()
    endTick = time.time()
    print "End take snapshot for count:" + str(cnt) + ", Elapse secs:" + str(endTick-startTick)
    # Writes the screenshot to a file
    fn = "d:\\s" + str(cnt) + ".png"
    startTick = time.time()
    print "Start write to file :" + fn
    screenShot.writeToFile(fn,'png')
    endTick = time.time()
    print "Ended write to file, Elapse secs:" + str(endTick-startTick)

    # external template Matching
    process = subprocess.Popen(['python','d:\\Projects\\mrTest\\cv.py','d:\\Projects\\mrTest\\tpl.png',fn],stdout=subprocess.PIPE)
    print process.communicate()

    cnt += 1
    print "Start to Sleep 5 secs"
    MonkeyRunner.sleep(5)
