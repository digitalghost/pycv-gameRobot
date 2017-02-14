import sys
import subprocess
import time
import random
# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

supportedDevices = [
    {"pName":"1080P Phone","resolution":"1920__1080"},
    {"pName":"720P Phone","resolution":"1280__720"},
    {"pName":"2K Phone","resolution":"2560__1440"},
]

autopath = {
    "auto_yuhun":[
        {"features":["tpl1_1.png","tpl1_2.png"],"touches":["tch1.png"],"waitTime":5},
        {"features":["tpl2.png"],"touches":["tch2.png"],"waitTime":5},
        {"features":["tpl3_2.png"],"touches":["tch3_2.png"],"waitTime":5},
        {"features":["tpl4.png"],"touches":["tch4.png"],"waitTime":5},
        {"features":["tpl5.png"],"touches":["tch5.png"],"waitTime":5},
        {"features":["tpl6.png"],"touches":["tch6.png"],"waitTime":5},
        {"features":["tpl7.png"],"touches":["tch7.png"],"waitTime":5}
    ]
}

def _checkTemplateExists(tplPath,snapshot):
    tplPath = './templates/' + DEVICE_RESID + "/" + SCENE_NAME + '/' + tplPath 
    process = subprocess.Popen(['python','./cvTplMatch.py',tplPath,snapshot],stdout=subprocess.PIPE) 
    cmdData = process.communicate()[0]
    cmdStr = str(cmdData)[:-1]
    cmdRC = process.returncode
    #print "!!!!!!!!!!!!"+cmdStr
    if str(cmdStr) == "NULL":
        return False,[]
    else:
        arr = cmdStr.split(",")
        for idx in range(len(arr)):
            arr[idx] = int(arr[idx])
        return True,arr

def _fixRotation(snapshotPath):
    process = subprocess.Popen(['python','./cvFixRotation.py',snapshotPath],stdout=subprocess.PIPE)
    cmdData = process.communicate()[0]
    cmdStr = str(cmdData)[:-1]
    cmdRC = process.returncode
    return cmdStr

print sys.argv
if len(sys.argv)<int(2) :
    print "Not enough arguments. cmd format is: monkeyrunner scriptname scenename"
    sys.exit(0)
SCENE_NAME = sys.argv[1];

# Kill monkey process for stop the exception for socket error
subprocess.call(['./killmonkey.sh'])
# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
print "***CONNECTED TO PHONE***"
device.wake()

# Screen properties for the device
SCREEN_WIDTH = int(device.getProperty("display.width"))
SCREEN_HEIGHT = int(device.getProperty("display.height"))
DEVICE_RESID = str(device.getProperty("display.width")) + "__" + str(device.getProperty("display.height"))
ANDROID_MAINVERSION = int(device.getProperty("build.version.release")[0])
print "***PHONE INFO*** device width:" + str(SCREEN_WIDTH) + ", Height:" + str(SCREEN_HEIGHT)+",Density:" + str(device.getProperty("display.density") + ", DeviceResID:" + DEVICE_RESID) + ",Android Version: " + str(ANDROID_MAINVERSION)
# Check if device supported
_supported = False
FIX_ROTATION_NEEDED = False
if ANDROID_MAINVERSION < 6:
    FIX_ROTATION_NEEDED = True
for _device in supportedDevices:
    if _device["resolution"] == DEVICE_RESID:
        _supported = True
        if _device.has_key("fixRotation"):
            FIX_ROTATION_NEEDED = _device["fixRotation"]
        break
if _supported == False:
    print "Your device " + DEVICE_RESID + " not supported in current version, plz contact me"
    sys.exit(0)

cnt = 0
LATEST_SCREENSHOT_PATH = "./"
while 1:
    # Old solution to takesnapshot
    startTick = time.time()
    screenShot = device.takeSnapshot()
    endTick = time.time()
    print "***TAKE SNAPSHOT DONE*** Elapse in secs:" + str(endTick-startTick)
    # Writes the screenshot to a file
    LATEST_SCREENSHOT_PATH = "./snapshots/s" + str(cnt) + ".png"
    startTick = time.time()
    screenShot.writeToFile(LATEST_SCREENSHOT_PATH,'png')
    if FIX_ROTATION_NEEDED:
        _fixRotation(LATEST_SCREENSHOT_PATH)
    endTick = time.time()
    print "***WRITE FILE DONE*** Elapse in secs:" + str(endTick-startTick)

    # Improved solution to takesnapshot
    #LATEST_SCREENSHOT_PATH = "./snapshots/s" + str(cnt) + ".png"
    #startTick = time.time()
    #cmd = "adb shell screencap -p | perl -pe 's/\\x0D\\x0A/\\x0A/g' > " + LATEST_SCREENSHOT_PATH
    #process = subprocess.Popen([cmd],stdout=subprocess.PIPE,shell=True)
    #cmdData = process.communicate()[0]
    #cmdStr = str(cmdData)[:-1]
    #cmdRC = process.returncode
    #if FIX_ROTATION_NEEDED:
    #    _fixRotation(LATEST_SCREENSHOT_PATH)
    #endTick = time.time()
    #print "***TAKE SNAPSHOT DONE*** Elapse in secs:" + str(endTick-startTick)

    #start loop for autopath
    steps =  autopath[SCENE_NAME]
    print "***AUTO FOR SCENE START*** Loop for %s ..." %SCENE_NAME
    for step in steps:
        # Checking for features, needs all features to be founded
        featuresFounded = False
        for idx, feature in enumerate(step["features"]):
                #print(idx, val)
                # Mathing the feature
                tplPath = feature
                print "***FEATURE %s MATCHING***........Template Path is %s" %(feature,tplPath)
                exists,region = ToolUtils.checkTemplateExists(tplPath,LATEST_SCREENSHOT_PATH)
                if exists:
                    print "***FEATURE MATCHING SUCCEED***" 
                    featuresFounded = True
                else:
                    print "***FEATURE MATCHING MISSED***" 
                    featuresFounded = False
                    break
        # Start to touches when features founded 
        if featuresFounded:
            if step.has_key("method"):
                print "***EXECUTING METHOD FOR %s MATCHING***........data is %s" %(step["method"],str(step))
                #print "eval string:" + step["method"] + "(" + str(step) + ")"
                code = step["method"] + "(" + str(step) + ")"
                if step.has_key("method_repeats"):
                    for idx in range(step["method_repeats"]):
                        exec code
                else:
                    exec code
            else:
                for idx, touch in enumerate(step["touches"]):
                    touchPath = touch
                    print "***TOUCH %s MATCHING***........Touch Path is %s" %(touch,touchPath)
                    exists,region = ToolUtils.checkTemplateExists(touchPath,LATEST_SCREENSHOT_PATH)
                    if exists:
                        arr = region
                        centerX = int(int(arr[0]) + (int(arr[2]) - int(arr[0]))/2)
                        centerY = int(int(arr[1]) + (int(arr[3]) - int(arr[1]))/2)
                        print "***FEATURE FOUNDED*** Start to touch at %s" %touch
                        device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
                    else:
                        print "---FEATURE FOUNDED, BUT TOUCH %s NOT FOUNDED, CHECK YOUR TEMPLATE CONFIGURATION---" %touch
            break
    
    cnt += 1
    if cnt == 10:
        cnt = 0

    print "===END SCENE LOOP==="
    MonkeyRunner.sleep(step["waitTime"])
