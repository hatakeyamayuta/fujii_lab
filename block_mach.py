import numpy as np
import cv2
from time import sleep
r_img = cv2.resize(cv2.imread("aloeR.jpg",0), (640,360))
l_img = cv2.resize(cv2.imread("aloeL.jpg",0), (640, 360))
#r_img = cv2.Canny(r_img,50,100)
#l_img = cv2.Canny(l_img,50,100)
r_array = np.array(r_img,dtype=np.int16)
l_array = np.array(l_img,dtype=np.int16)
y ,x = r_img.shape[:2]
score = np.empty((x ,y))
m = 8  #kernel (200,200)
pos = np.zeros((y,x))
print(x,y)

for l in range(0,y,m):
    for k in range(0,x,m):
        print("reset")
        old = 10000
        for i in range(0,x-m):
            diff = (r_array[l:l+m,i:i+m] - l_array[l:l+m,k:k+m])**2
            #print(diff)
            score[i,l] = diff.sum()
            t = diff.sum()
            if diff.sum() < 5500 :
                if t < old:
                    dist = k - i
                    print(k+m/2+1,i+m/2+1,l+m/2+1)
                    pos[l:l+m, k:k+m] =  dist
                    old = t 
        
print(np.nonzero(pos))    
#print("\n".join([" ".join(map(str,l)) for l in pos]))
print(pos.shape)

from PIL import Image

Image.fromarray(np.uint8(pos)).save("gray.png")
