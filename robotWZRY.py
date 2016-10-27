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
    "auto_coin":[
        {"features":["tpl1.png"],"touches":["tch1.png"]},
        {"features":["tpl2.png"],"touches":["tch2.png"]},
        {"features":["tpl3_1.png","tpl3_2.png"],"touches":["tch3.png"]},
        {"features":["tpl5.png"],"touches":["tch5.png"]},
        {"features":["tpl6_1.png","tpl6_2.png"],"touches":["tch6.png"]},
        {"features":["tpl7_1.png","tpl7_2.png"],"touches":["tch7.png"]},
        {"features":["tpl8.png"],"touches":["tch8.png"]},
        {"features":["tpl9.png"],"touches":["tch9.png"]},
        {"features":["tpl10.png"],"touches":["tch10.png"]}
    ],
    "auto_vsnpc":[
        {"features":["tpl1_1.png","tpl1_2.png"],"touches":["tch1.png"]},
        {"features":["tpl2.png"],"touches":["tch2.png"]},
        {"features":["tpl3.png"],"touches":["tch3.png"]},
        {"features":["tpl4.png"],"touches":["tch4.png"]},
        {"features":["tpl5.png"],"touches":["tch5.png"]},
        {"features":["tpl6.png"],"touches":["tch6.png"]},
        {"features":["tpl7_1.png","tpl7_2.png"],"touches":["tch7.png"],"method":"proc_autovsnpc_for_tpl7"},
        {"features":["tpl8_1.png"],"touches":["tch8.png"]},
        {"features":["tpl9.png"],"touches":["tch9.png"]},
        {"features":["tpl10_1.png","tpl10_2.png"],"touches":["tch10.png","tch10_1.png","tch10_2.png"],"method":"proc_autovsnpc_for_tpl10","method_repeats":1},

    ]
}

def proc_autovsnpc_for_tpl10(data):
    # Combat screen, Hope more AI involved 
    features = data["features"]
    touches = data["touches"]
    print "***ENTER SUB PROC proc_autovsnpc_for_tpl10***" 
    
    # Drag joystick to make hero move ,and attack.One step, one attack
    _joyY = SCREEN_HEIGHT - int(int(SCREEN_HEIGHT)/4)
    _joyX = int(SCREEN_HEIGHT/4)
    _moveXVal = _joyX
    _moveYVal = _moveXVal
    #print "joyX:%s,joyY:%s,ScreenHeight:%s" %(str(_joyX),str(_joyY),str(SCREEN_HEIGHT))
    _random = random.randint(0,5)
    if _random == 0:
        _moveXVal = 0
    elif _random == 1:
        _moveXVal = 0-_moveXVal
    else:
        _moveXVal = _moveXVal
    _random = random.randint(0,2)
    if _random == 0:
        _moveYVal = 0
    elif _random == 1:
        _moveYVal = _moveXVal
    else:
        _moveYVal = 0 - _moveXVal
    if _moveXVal == 0 and _moveYVal == 0:
        _random = random.randint(0,1)
        if _random == 0:
            _moveXVal = _joyX
        else:
            _moveYVal = _joyX
    _target = (_joyX+_moveXVal,_joyY+_moveYVal)
    _rpts = random.randint(2,5)
    print "Drag joy %s times, from point: %s,%s  to target point: %s,%s" %(str(_rpts),str(_joyX),str(_joyY),str(_target[0]),str(_target[1]))
    # Check if able to touch the "Attack" button
    touchPath = touches[0]
    print "Matching touch path for attack button  %s" %touchPath
    exists,region = _checkTemplateExists(touchPath,LATEST_SCREENSHOT_PATH)
    centerX = centerY = 0
    if exists:
        centerX = region[0] + (region[2] - region[0])/2
        centerY = region[1] + (region[3] - region[1])/2
    for idx in range(_rpts):
        device.drag((_joyX,_joyY),_target , 2, 10)
        if exists:
            print "Attack button founded, Start to attack" 
            device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
            device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
        else:
            print "Attack button not founded"
    device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
    device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)

    # To buy the item
    touchPath = features[0] 
    exists,region = _checkTemplateExists(touchPath,LATEST_SCREENSHOT_PATH)
    if exists:
        centerX = region[0] + (region[2] - region[0])/2 + (region[2] - region[0])*2
        centerY = region[1] + (region[3] - region[1])/2 + (region[3] - region[1])*2
        print "To buy some items."
        device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
    else:
        print "Coin bag not found"

    # Upgrade skill level
    for val in [1,2]: 
        touchPath = touches[val] 
        exists,region = _checkTemplateExists(touchPath,LATEST_SCREENSHOT_PATH)
        if exists:
            centerX = region[0] + (region[2] - region[0])/2
            centerY = region[1] + (region[3] - region[1])/2
            print "Skill level up"
            device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
            device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
        else:
            print "Levelup button not found"




def proc_autovsnpc_for_tpl7(data):
    # Choose hero screen 
    features = data["features"]
    touches = data["touches"]
    print "***ENTER SUB PROC proc_autovsnpc_for_tpl7***" 
    # Check if able to touch the "Confirm" button
    touchPath = touches[0] 
    print "Matching touch path for confirm button  %s" %touchPath
    exists,region = _checkTemplateExists(touchPath,LATEST_SCREENSHOT_PATH)
    if exists:
        arr = region
        centerX = int(int(arr[0]) + (int(arr[2]) - int(arr[0]))/2)
        centerY = int(int(arr[1]) + (int(arr[3]) - int(arr[1]))/2)
        print "Confirm button founded, Start to touch" 
        device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
    else:
        print "Confirm button not founded"
    featurePath = features[0] 
    exists,region = _checkTemplateExists(featurePath,LATEST_SCREENSHOT_PATH)
    if exists:
        _leftX = 0
        _leftY = 120
        _bottomX = int(region[0])
        _bottomY = int(SCREEN_HEIGHT)
        _tX = random.randint(_leftX,_bottomX)
        _tY = random.randint(_leftY,_bottomY)
        print "Touch random point at left hero select panel, X:%s, Y:%s" %(str(_tX),str(_tY))
        device.touch(_tX,_tY,MonkeyDevice.DOWN_AND_UP)
    else:
        print "Not detected archon tpl for:" + features[0]
    print "***EXIT SUB PROC proc_autovsnpc_for_tpl7***" 


def proc_autovsnpc_for_tpl2(data):
    print "IN Method proc_autovsnpc_for_tpl2,data is: " + str(data)

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
                exists,region = _checkTemplateExists(tplPath,LATEST_SCREENSHOT_PATH)
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
                    exists,region = _checkTemplateExists(touchPath,LATEST_SCREENSHOT_PATH)
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
    MonkeyRunner.sleep(5)
