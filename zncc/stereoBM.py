import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('aloeL.jpg',0)
imgR = cv2.imread('aloeR.jpg',0)

stereo = cv2.StereoSGBM_create(minDisparity=10,numDisparities=16, blockSize=3)
#stereo = cv2.StereoSGBM_create()
disparity = stereo.compute(imgL,imgR)
cv2.imwrite("test.png",disparity)
plt.imshow(disparity,'gray')
plt.show()
