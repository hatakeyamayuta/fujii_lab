import numpy as np
import cv2

img = cv2.imread('stereo_calib_left4.png')
img = cv2.medianBlur(img,5,(3,3))
Z = img.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 16
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))
h, w =img.shape[:2]
result = np.zeros((K,h,w))
#dist_img = cv2.imread("stereo_gray2018-07-16.png",0)
dist_img = np.load("test1.npy")
print(center)
for i in range(h):
    for j in range(w):
        for count,con in enumerate(center):
            k = res2[i,j]==con
            if k[0] == True and k[1] == True:
                result[count,i,j] = dist_img[i,j]

kernel = np.ones((3,3),np.uint8)
kernel1 = np.ones((5,5),np.uint8)
kernel2 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)

for layer in range(K):
    mor = cv2.morphologyEx(result[layer],cv2.MORPH_CLOSE,kernel)
    mor = cv2.morphologyEx(mor,cv2.MORPH_OPEN,kernel)
    mor = cv2.morphologyEx(mor,cv2.MORPH_OPEN,kernel)
    mor = cv2.morphologyEx(mor,cv2.MORPH_OPEN,kernel)
    mor = cv2.morphologyEx(mor,cv2.MORPH_OPEN,kernel)
    result[layer] = cv2.morphologyEx(mor,cv2.MORPH_OPEN,kernel)
    #result[layer] = cv2.erode(mor,kernel1,iterations=1)
for i in range(h):
    for j in range(w):
        for count,con in enumerate(center):
            k = res2[i,j]==con
            if k[0] == True and k[1] == True and k[2] == True:
                dist_img[i, j] = result[count,i,j]
np.save("k-means_array",dist_img)
cv2.imwrite("k-means.png",dist_img)
cv2.imshow("test",dist_img)
cv2.imshow("res",res2)
for  n in range(K):
    cv2.imshow('res2',result[n])
    cv2.waitKey(0)
cv2.destroyAllWindows()
