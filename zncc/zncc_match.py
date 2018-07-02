import numpy as np
import cv2
from time import sleep
from plot import plot_3d
def zncc():
    pnt1 = []
    pnt2 = []
    r_img = cv2.resize(cv2.imread("stereo_calib_right.png",0),(640,480))
    l_img = cv2.resize(cv2.imread("stereo_calib_left.png",0),(640, 480))
    #r_img = cv2.imread("testleft.jpg",0)
    #l_img = cv2.imread("testright.jpg",0)
    #r_img = cv2.Canny(r_img,50,100)
    #l_img = cv2.Canny(l_img,50,100)
    r_img = cv2.medianBlur(r_img,5,(5,5))
    l_img = cv2.medianBlur(l_img,5,(5,5))
    r_array = np.array(r_img,dtype=np.float64)
    l_array = np.array(l_img,dtype=np.float64)
    y ,x = r_img.shape[:2]
    score = np.empty((x ,y))
    m = 10 #kernel (4,4)
    pos = np.zeros((y,x))
    #print(x,y)

    for l in range(0,y-m,3):
        for k in range(m,x-m,3):
            old = 0
            flag = None
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

                if temp >= 0.6 and k-i > 50 :
                    if temp > old:
                        flag = True
                        #print(temp)
                        dist = k - i
                        #print(k,i,l)
                        #pos[l:l+m, k:k+m] =  dist
                        pos[l, k] =  dist
                        old = temp
            #if flag == True:
            #    pnt1.append((l,k))
            #    pnt2.append((l,k+dist))

    #print(pnt1)

    print(np.nonzero(pos))    
    #print("\n".join([" ".join(map(str,l)) for l in pos]))
    print(pos.shape)
    #plot_3d(pos)

    from PIL import Image

    Image.fromarray(np.uint8(pos)).save("stereo_gray.png")


def main():
    zncc()

if __name__=="__main__":
    main()
