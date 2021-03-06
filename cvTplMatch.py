import sys
import cv2
import numpy as np

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


if len(sys.argv)<3 :
    sys.exit("Not enough arguments.")

# print "Arguments count is:" + str(len(sys.argv)) + ", template is:" + str(sys.argv[1]) + ", fullscreen is :" + str(sys.argv[2])

img = cv2.imread(sys.argv[2],0)
img2 = img.copy()
template = cv2.imread(sys.argv[1],0)
w, h = template.shape[::-1]

method = cv2.TM_CCOEFF_NORMED
# All the 6 methods for comparison in a list
#methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
res = cv2.matchTemplate(img,template,method)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

resCrop = img2[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
code = mse(resCrop,template)

if code > 1000:
    #print "NULL,code is:" + str(code)
    print "NULL"
else:
    print str(top_left[0]) + "," + str(top_left[1]) + "," + str(bottom_right[0]) + "," + str(bottom_right[1])
    

#for meth in methods:
#    img = img2.copy()
#    method = eval(meth)
#
#    # Apply template Matching
#    res = cv2.matchTemplate(img,template,method)
#    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#
#    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#        top_left = min_loc
#    else:
#        top_left = max_loc
#    bottom_right = (top_left[0] + w, top_left[1] + h)
#
#    print str(top_left[0]) + "," + str(top_left[1]) + "," + str(bottom_right[0]) + "," + str(bottom_right[1])
#    resCrop = img2[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
#    code = mse(resCrop,template)
#    cv2.rectangle(img,top_left, bottom_right, 255, 8)
#    plt.subplot(121),plt.imshow(resCrop,cmap = 'gray')
#    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#    #plt.subplot(122),plt.imshow(img,cmap = 'gray')
#    #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#    plt.subplot(122),plt.imshow(template,cmap = 'gray')
#    plt.title('Template'), plt.xticks([]), plt.yticks([])
#    #plt.suptitle(meth)
#    #plt.show()
#
#
#    plt.suptitle("Method: %s,MSE: %.2f" % (meth,code))
#
#    plt.show()
