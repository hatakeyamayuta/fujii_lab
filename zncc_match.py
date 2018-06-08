import numpy as np
import cv2
from time import sleep
r_img = cv2.resize(cv2.imread("cam_right.JPG",0), (640,360))
l_img = cv2.resize(cv2.imread("cam_left.JPG",0), (640, 360))
#r_img = cv2.resize(cv2.imread("lage_wide/right.jpg",0), (640,360))
#l_img = cv2.resize(cv2.imread("lage_wide/left.jpg",0), (640, 360))
#r_img = cv2.Canny(r_img,50,100)
#l_img = cv2.Canny(l_img,50,100)
r_array = np.array(r_img,dtype=np.float64)/255
l_array = np.array(l_img,dtype=np.float64)/255
y ,x = r_img.shape[:2]
score = np.empty((x ,y))
m = 8  #kernel (4,4)
pos = np.zeros((y,x))
print(x,y)

for l in range(0,y,4):
    for k in range(0,x-4,4):
        print("reset")
        old = 0
        for i in range(0,x-m):
            w_r = r_array[l:l+m,i:i+m]
            w_l = l_array[l:l+m,k:k+m]

            
            mean_r = np.mean(w_r)
            mean_l = np.mean(w_l)
            w_r = w_r - mean_r
            w_l = w_l - mean_l
            num = np.sum(w_r*w_l)
            den = np.sqrt(np.sum(w_r**2))*np.sqrt(np.sum(w_l**2))
            temp = num/den

            if temp > 0.7 and k -i < 100:
                if temp > old:
                        dist = k - i
                        print(k,i,j)
                        pos[l:l+m, k:k+m] =  dist/16
                        old = temp





            """
            #print(diff)
            score[i,l] = diff.sum()
            t = diff.sum()
            if diff.sum() < 1500 :
                if t < old:
                    dist = k - i
                    print(k+m/2+1,i+m/2+1,l+m/2+1)
                    pos[l:l+m, k:k+m] =  dist
                    #pos[l, k] =  dist
                    old = t 

            """
print(np.nonzero(pos))    
#print("\n".join([" ".join(map(str,l)) for l in pos]))
print(pos.shape)

from PIL import Image

Image.fromarray(np.uint8(pos)).save("gray.png")

