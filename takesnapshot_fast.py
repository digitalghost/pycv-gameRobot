import subprocess
import time

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import subprocess

def _run_command(command):
    #print "Command is:" + command
    p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    print "cmd : " + command
    #return iter(p.stdout.readline, b'')
 

# Connects to the current device, returning a MonkeyDevice object
print "Start Connction to Phone"
device = MonkeyRunner.waitForConnection()
print "Connected to Phone"
device.wake()

pWidth = device.getProperty("display.width")
pHeight = device.getProperty("display.height")
print "device width:" + str(pWidth) + ", Height:" + str(pHeight) + ", Density:" + str(device.getProperty("display.density"))
print "device name :" +str(device.getProperty("build.product"))+ str(device.getProperty("build.device"))
cnt = 0
fn = "./"
while 1:
    startTick = time.time()
    print "Start take snapshot for count:" + str(cnt)
    screenShot = device.takeSnapshot()
    endTick = time.time()
    fn = "./snapshots/s" + str(cnt) + ".png"
    cmd = "adb shell screencap -p | perl -pe 's/\\x0D\\x0A/\\x0A/g' > " + fn
    _run_command(cmd)
    print "End take snapshot for count:" + str(cnt) + ", Elapse secs:" + str(endTick-startTick)
    cnt = cnt + 1 
    print "Next Loop..."
