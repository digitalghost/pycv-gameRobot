import subprocess
import time

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice


# Kill monkey process for stop the exception for socket error
subprocess.call(['./killmonkey.sh'])
# Connects to the current device, returning a MonkeyDevice object
print "Start Connction to Phone"
device = MonkeyRunner.waitForConnection()
print "Connected to Phone"
device.wake()

pWidth = device.getProperty("display.width")
pHeight = device.getProperty("display.height")
print "device width:" + str(pWidth) + ", Height:" + str(pHeight) + ", Density:" + str(device.getProperty("display.density"))

defaultDensity = 3.5
currentDensity = float(device.getProperty("display.density"));
scaleRate = currentDensity/defaultDensity

print "Current density: %f, default density: %f, current/default= %f" %(currentDensity,defaultDensity,scaleRate)

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
    process = subprocess.Popen(['python','./cvScale.py','./tpl.png',fn,str(scaleRate)],stdout=subprocess.PIPE)
    print process.communicate()

    cnt += 1
    print "Start to Sleep 5 secs"
    MonkeyRunner.sleep(5)
