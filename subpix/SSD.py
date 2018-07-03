import numpy as np
import cv2
from time import sleep
r_img = cv2.resize(cv2.imread("stereo_calib_right.png",0), (640,480))
l_img = cv2.resize(cv2.imread("stereo_calib_left.png",0), (640,480))
r_array = np.array(r_img,dtype=np.int16)
l_array = np.array(l_img,dtype=np.int16)
y ,x = r_img.shape
score = np.empty((x ,y))
m = 8  #kernel (200,200)
pos = np.zeros((y,x))
print(x,y)

def SSD(r_array,l_array,l,i,k,m):
    diff = abs(r_array[l:l+m,i:i+m] - l_array[l:l+m,k:k+m])
    t = diff.sum()
    return t

for l in range(0,y-m,3):
    for k in range(0,x-m,3):
        old = 10000
        for i in range(0,x-m):
            #diff = abs(r_array[l:l+m,i:i+m] - l_array[l:l+m,k:k+m])
            #score[i,l] = diff.sum()
            t = SSD(r_array, l_array,l,i,k,m)
            if i ==0 or i == x-m:
                continue
            if t < 500:
                if t < old:
                    R1 = SSD(r_array,l_array,l,i+1,k,m)
                    R_1 = SSD(r_array,l_array,l,i-1,k,m)
                    if R1 < R_1:
                        d = ((R1-R_1)/(t-R_1))*0.5
                    else:
                        d = ((R1-R_1)/(t-R1))*0.5
                    dist = k - i + d
                    pos[l:l+m, k:k+m] =  dist
                    old = t 

        
print(np.nonzero(pos))    
#print("\n".join([" ".join(map(str,l)) for l in pos]))
print(pos.shape)

from PIL import Image

Image.fromarray(np.uint8(pos)).save("gray.png")
