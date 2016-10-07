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
fn = "./"
while 1:
    startTick = time.time()
    print "Start take snapshot for count:" + str(cnt)
    screenShot = device.takeSnapshot()
    endTick = time.time()
    print "End take snapshot for count:" + str(cnt) + ", Elapse secs:" + str(endTick-startTick)
    # Writes the screenshot to a file
    fn = "./snapshots/s" + str(cnt) + ".png"
    startTick = time.time()
    print "Start write to file :" + fn
    screenShot.writeToFile(fn,'png')
    endTick = time.time()
    print "Ended write to file, Elapse secs:" + str(endTick-startTick)
 
    # external template Matching
    process = subprocess.Popen(['python','./cvTplMatch.py','./tpl.png',fn],stdout=subprocess.PIPE)
    cmdData = process.communicate()[0]
    cmdStr = str(cmdData)[:-1]
    cmdRC = process.returncode

    if str(cmdStr) == "NULL":
        print "No matched template image,touch nothing, wait for next check..."
    else:
        arr = cmdStr.split(",")
        centerX = int(int(arr[0]) + (int(arr[2]) - int(arr[0]))/2)
        centerY = int(int(arr[1]) + (int(arr[3]) - int(arr[1]))/2)
        device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
        print "Touch the screen point at: " + cmdStr





    cnt += 1
    print "Start to Sleep 5 secs"
    MonkeyRunner.sleep(5)
