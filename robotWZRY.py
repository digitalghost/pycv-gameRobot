import subprocess
import time
# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

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
    ]

}


# Kill monkey process for stop the exception for socket error
subprocess.call(['./killmonkey.sh'])
# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
print "***CONNECTED TO PHONE***"
device.wake()

pWidth = device.getProperty("display.width")
pHeight = device.getProperty("display.height")
print "***PHONE INFO*** device width:" + str(pWidth) + ", Height:" + str(pHeight) + ", Density:" + str(device.getProperty("display.density"))

defaultDensity = 3.5
currentDensity = float(device.getProperty("display.density"));
scaleFactor = currentDensity/defaultDensity

cnt = 0
fn = "./"
while 1:
    startTick = time.time()
    #print "Start take snapshot for count:" + str(cnt)
    screenShot = device.takeSnapshot()
    endTick = time.time()
    #print "End take snapshot for count:" + str(cnt) + ", Elapse secs:" + str(endTick-startTick)
    print "***TAKE SNAPSHOT DONE*** Elapse in secs:" + str(endTick-startTick)
    # Writes the screenshot to a file
    fn = "./snapshots/s" + str(cnt) + ".png"
    startTick = time.time()
    #print "Start write to file :" + fn
    screenShot.writeToFile(fn,'png')
    endTick = time.time()
    #print "Ended write to file, Elapse secs:" + str(endTick-startTick)
    print "***WRITE FILE DONE*** File: " + fn + " Elapse in secs:" + str(endTick-startTick)

    #start loop for autopath
    for sceneName, steps in autopath.iteritems():
        print "***AUTO FOR SCENE START*** Loop for %s ..." %sceneName
        for step in steps:
            # Checking for features, needs all features to be founded
            featuresFounded = False
            for idx, feature in enumerate(step["features"]):
                    #print(idx, val)
                    # Mathing the feature
                    tplPath = './templates/' + sceneName + '/' + feature
                    print "***FEATURE %s MATCHING***........Template Path is %s" %(feature,tplPath)
                    process = subprocess.Popen(['python','./cvTplMatchScale.py',tplPath,fn,str(scaleFactor)],stdout=subprocess.PIPE)
                    cmdData = process.communicate()[0]
                    cmdStr = str(cmdData)[:-1]
                    cmdRC = process.returncode
                    if str(cmdStr) == "NULL":
                        print "***FEATURE MATCHING MISSED***"
                        featuresFounded = False
                        break
                    else:
                        print "***FEATURE MATCHING SUCCEED***"
                        featuresFounded = True
            # Start to touches when features founded
            if featuresFounded:
                for idx, touch in enumerate(step["touches"]):
                        touchPath = './templates/' + sceneName + '/' + touch
                        print "***TOUCH %s MATCHING***........Touch Path is %s" %(touch,touchPath)
                        process = subprocess.Popen(['python','./cvTplMatchScale.py',touchPath,fn,str(scaleFactor)],stdout=subprocess.PIPE)
                        cmdData = process.communicate()[0]
                        cmdStr = str(cmdData)[:-1]
                        cmdRC = process.returncode
                        if str(cmdStr) == "NULL":
                            print "---FEATURE FOUNDED, BUT TOUCH %s NOT FOUNDED, CHECK YOUR TEMPLATE CONFIGURATION---" %touch
                        else:
                            arr = cmdStr.split(",")
                            print "cmd return:" + cmdStr
                            centerX = int(int(arr[0]) + (int(arr[2]) - int(arr[0]))/2)
                            centerY = int(int(arr[1]) + (int(arr[3]) - int(arr[1]))/2)
                            print "***FEATURE FOUNDED*** Start to touch at %s" %touch
                            device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
                break
    cnt += 1
    if cnt == 10:
        cnt = 0

    print "===SLEEP FOR 55555 SECS==="
    MonkeyRunner.sleep(5)
