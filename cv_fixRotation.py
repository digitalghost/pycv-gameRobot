import sys
import subprocess
import cv2
import numpy as np
from matplotlib import pyplot as plt


#adb shell dumpsys input | grep 'SurfaceOrientation' | awk '{ print $2 }'
# 1 For 90 degree, 3 For 270 degree
def _rotateAndScale(img, scaleFactor = 0.5, degreesCCW = 30):
    (oldY,oldX) = img.shape #note: numpy uses (y,x) convention but most OpenCV functions use(x,y)
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=degreesCCW, scale=scaleFactor)
    #rotate about center of image.
    #choose a new image size.
    newX,newY = oldX*scaleFactor,oldY*scaleFactor
    #include this if you want to prevent corners being cut off
    r = np.deg2rad(degreesCCW)
    newX,newY = (abs(np.sin(r)*newY) + abs(np.cos(r)*newX),abs(np.sin(r)*newX) + abs(np.cos(r)*newY))

    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx
    M[1,2] += ty
    rotatedImg = cv2.warpAffine(img, M,dsize=(int(newX),int(newY)))
    return rotatedImg


def _run_command(command):
    print "Command is:" + command
    p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    return iter(p.stdout.readline, b'')
        
if len(sys.argv)<2 :
    sys.exit("Not enough arguments.")

print "Arguments count is:" + str(len(sys.argv)) + ". Params needs, Filename is:" + str(sys.argv[1]) 

cmd = "adb shell dumpsys input | grep 'SurfaceOrientation' | awk '{ print $2 }'"
result = _run_command(cmd)
resCode = "0" #0,1,3
for res in result:
    resCode = res

orgImg = cv2.imread(sys.argv[1],0)
cv2.imwrite(sys.argv[1]+"1.png",orgImg)
orgImg2 = orgImg.copy()
#resultImg = _rotateImage2(orgImg,90)
resultImg = _rotateAndScale(orgImg,1.0,90)
if resCode == "1":
    resultImg = _rotateAndScale(orgImg,1.0,90)
elif resCode == "3":
    resultImg = _rotateAndScale(orgImg,1.0,270)
cv2.imwrite(sys.argv[1],resultImg)



plt.subplot(121),plt.imshow(resultImg,cmap = 'gray')
plt.title('After:'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(orgImg2,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.suptitle("Execute rotation")
plt.show()

