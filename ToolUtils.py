# -*- coding: utf-8 -*
import subprocess
import time
import Settings
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

class ToolUtils(object):
    """docstring for ClassName"""
    def __init__(self):
        super(ClassName, self).__init__()
        
    @staticmethod
    def getTouchPoint(region):
        centerX = int(int(region[0]) + (int(region[2]) - int(region[0]))/2)
        centerY = int(int(region[1]) + (int(region[3]) - int(region[1]))/2)
        return centerX,centerY

    @staticmethod
    def checkTemplateExists(tplPath,snapshot):
        tplPath = './templates/' + Settings.DEVICE_RESID + "/" + Settings.SCENE_NAME + '/' + tplPath
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


    @staticmethod
    def fixRotation(snapshotPath):
        process = subprocess.Popen(['python','./cvFixRotation.py',snapshotPath],stdout=subprocess.PIPE)
        cmdData = process.communicate()[0]
        cmdStr = str(cmdData)[:-1]
        cmdRC = process.returncode
        return cmdStr

    @staticmethod
    def takeSnapshot(device):
        startTick = time.time()
        screenShot = device.takeSnapshot()
        endTick = time.time()
        print "***TAKE SNAPSHOT DONE*** Elapse in secs:" + str(endTick-startTick)
        # Writes the screenshot to a file
        Settings.LATEST_SCREENSHOT_PATH = "./snapshots/s" + str(Settings.SNAP_COUNT) + ".png"
        startTick = time.time()
        screenShot.writeToFile(Settings.LATEST_SCREENSHOT_PATH,'png')
        if Settings.FIX_ROTATION_NEEDED:
            ToolUtils.fixRotation(Settings.LATEST_SCREENSHOT_PATH)
        endTick = time.time()
        print "***WRITE FILE DONE*** Elapse in secs:" + str(endTick-startTick)
        Settings.SNAP_COUNT += 1
        if Settings.SNAP_COUNT == 10:
            Settings.SNAP_COUNT = 0

    @staticmethod
    def executeScenePath(scenePath, device):
        featuresFounded = False
        print "===BEGIN PATH %s LOOP===" %(scenePath.name)
        while (not featuresFounded):
            if scenePath.needReSnapshots:
                ToolUtils.takeSnapshot(device)

            # Execute the scene path
            for feature in scenePath.features:
                tplPath = feature
                print "***FEATURE %s MATCHING***........Template Path is %s" %(feature,tplPath)
                exists,region = ToolUtils.checkTemplateExists(tplPath,Settings.LATEST_SCREENSHOT_PATH)
                if exists:
                    print "***FEATURE MATCHING SUCCEED***" 
                    featuresFounded = True
                else:
                    print "***FEATURE MATCHING MISSED***" 
                    featuresFounded = False
                    break
            if featuresFounded:
                if scenePath.method != "":
                    print "***EXECUTING METHOD FOR %s MATCHING***........data is %s" %(scenePath.name,scenePath.method)
                    getCustomMethod = getattr(Settings.GAME_OBJECT, scenePath.method)
                    getCustomMethod(scenePath)
                else:
                    for touch in scenePath.touches:
                        touchPath = touch
                        print "***TOUCH %s MATCHING***........Touch Path is %s" %(touch,touchPath)
                        exists,region = ToolUtils.checkTemplateExists(touchPath,Settings.LATEST_SCREENSHOT_PATH)
                        if exists:
                            centerX,centerY = ToolUtils.getTouchPoint(region)
                            print "***FEATURE FOUNDED*** Start to touch at %s" %touch
                            device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
                        else:
                            print "---FEATURE FOUNDED, BUT TOUCH %s NOT FOUNDED, CHECK YOUR TEMPLATE CONFIGURATION---" %touch
            if (featuresFounded or (not scenePath.needRepeatWhenNotFound)):
                break
            if not featuresFounded:
                print "!!!!!Not Found"
                MonkeyRunner.sleep(5)

        print "===END PATH %s LOOP===\n" %(scenePath.name)
        return scenePath.nextPathId
            