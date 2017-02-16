# -*- coding: utf-8 -*
import sys
import random
import subprocess
import Scene
import ScenePath
import Settings
from ToolUtils import ToolUtils

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

supportedDevices = [
    {"pName":"1080P Phone","resolution":"1920__1080"},
    {"pName":"720P Phone","resolution":"1280__720"},
    {"pName":"2K Phone","resolution":"2560__1440"},
]

print sys.argv
if len(sys.argv)<int(3) :
    print "Not enough arguments. cmd format is: monkeyrunner scriptname gamename sencename"
    sys.exit(0)
gameName = sys.argv[1];
sceneName = sys.argv[2];

Settings.init()

# dynamic import module name and load game's sence method
module = __import__(gameName)
gameClass = getattr(module, gameName)
Settings.GAME_OBJECT = gameClass()
getSenceMethod = getattr(Settings.GAME_OBJECT, sceneName)
sence = getSenceMethod()
print "※※※※※※※※※※※※BEGIN EXECUTE SCENE %s※※※※※※※※※※※※" %(sence.name)
Settings.SCENE_NAME = sceneName

# Kill monkey process for stop the exception for socket error
subprocess.call(['./killmonkey.sh'])
# Connects to the current device, returning a MonkeyDevice object
Settings.DEVICE = MonkeyRunner.waitForConnection()
print "***CONNECTED TO PHONE***"
Settings.DEVICE.wake()

# Screen properties for the device
SCREEN_WIDTH = int(Settings.DEVICE.getProperty("display.width"))
SCREEN_HEIGHT = int(Settings.DEVICE.getProperty("display.height"))
ANDROID_MAINVERSION = int(Settings.DEVICE.getProperty("build.version.release")[0])
Settings.DEVICE_RESID = str(Settings.DEVICE.getProperty("display.width")) + "__" + str(Settings.DEVICE.getProperty("display.height"))
print "***PHONE INFO*** device width:" + str(SCREEN_WIDTH) + ", Height:" + str(SCREEN_HEIGHT)+",Density:" + str(Settings.DEVICE.getProperty("display.density") + ", DeviceResID:" + Settings.DEVICE_RESID) + ",Android Version: " + str(ANDROID_MAINVERSION)
# Check if device supported
_supported = False
if ANDROID_MAINVERSION < 6:
    Settings.FIX_ROTATION_NEEDED = True
for _device in supportedDevices:
    if _device["resolution"] == Settings.DEVICE_RESID:
        _supported = True
        if _device.has_key("fixRotation"):
            Settings.FIX_ROTATION_NEEDED = _device["fixRotation"]
        break
if _supported == False:
    print "Your device " + Settings.DEVICE_RESID + " not supported in current version, plz contact me"
    sys.exit(0)

print "***Sence Paths Length %s" %len(sence.paths)

if len(sence.paths) >0:
    currentPath = sence.paths[0] 
    while(True): 
        nextPathId = ToolUtils.executeScenePath(currentPath, Settings.DEVICE)  
        if nextPathId >= 0:
            foundNextPath = False
            for path in sence.paths:
                if path.pathId == nextPathId:
                    foundNextPath = True
                    currentPath = path
                    print "wait for %s second" %str(currentPath.waitTime)
                    MonkeyRunner.sleep(currentPath.waitTime)
            if (not foundNextPath):
                print "※※※※※※※※※※※※END EXECUTE SCENE %s※※※※※※※※※※※ NOT FOUND NEXT PATH" %str(nextPathId)
                break
        else:
            print "※※※※※※※※※※※※END EXECUTE SCENE %s※※※※※※※※※※※" %(sence.name)
            break