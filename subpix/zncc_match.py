import numpy as np
import cv2
from time import sleep
def ZNCC(l_array,r_array,l,i,k,m):
    w_r = r_array[l:l+m,i:i+m]
    w_l = l_array[l:l+m,k:k+m]
    mean_r = np.mean(w_r)
    mean_l = np.mean(w_l)
    w_r = w_r - mean_r
    w_l = w_l - mean_l
    num = np.sum(w_r*w_l)
    den = np.sqrt(np.sum(w_r**2))*np.sqrt(np.sum(w_l**2))
    evaluation = num/den
    
    return evaluation


def matching():
    pnt1 = []
    pnt2 = []
    r_img = cv2.resize(cv2.imread("stereo_calib_right.png",0),(640,480))
    l_img = cv2.resize(cv2.imread("stereo_calib_left.png",0),(640, 480))
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
            for i in range(0,x-m):
                if i==0 or i ==x-m:
                    continue
                eva = ZNCC(l_array,r_array,l,i,k,m)
                eva1 = ZNCC(l_array,r_array,l,i+1,k,m)
                eva_1 = ZNCC(l_array,r_array,l,i-1,k,m)

                if eva >= 0.7 and k-i > 50 :
                    if eva > old:
                        dist = k - i
                        pos[l:l+m, k:k+m] =  dist
                        #pos[l, k] =  dist
                        old = eva
            #if flag == True:
            #    pnt1.append((l,k))
            #    pnt2.append((l,k+dist))


    print(np.nonzero(pos))    
    print(pos.shape)

    from PIL import Image

    Image.fromarray(np.uint8(pos)).save("stereo_gray.png")


def main():
    matching()

if __name__=="__main__":
    main()
