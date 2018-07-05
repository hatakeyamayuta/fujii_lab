import numpy as np
import cv2
import sys
import time
m = 16

def RNSCAC():
    pass


def SSD(r_array,l_array,l,i,k,m):
    diff = abs(r_array[l:l+m,i:i+m] - l_array[l:l+m,k:k+m])
    evaluation = diff.sum()
    return evaluation

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

def zncc_match():
    r_array,l_array,pos = read_stereo_img()
    y ,x = r_array.shape[:2]
    for l in range(0,y-m,m):
        for k in range(m,x-m,m):
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
    return pos
               
def sad_match():
    print("__start__","mask{0}".format(m))
    r_array,l_array,pos = read_stereo_img()
    y ,x = r_array.shape[:2]
    for l in range(0,y-m,3):
        for k in range(m,x-m,3):
            old =  2000
            for i in range(0,x-m):
                if i==0 or i ==x-m:
                    continue
                t = SSD(r_array, l_array,l,i,k,m)
                if t < 2000:
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


    return pos

def read_stereo_img():
    r_img = cv2.resize(cv2.imread("stereo_calib_right.png",0),(640,480))
    l_img = cv2.resize(cv2.imread("stereo_calib_left.png",0),(640, 480))
    r_img = cv2.medianBlur(r_img,5,(5,5))
    l_img = cv2.medianBlur(l_img,5,(5,5))
    r_array = np.array(r_img,dtype=np.float64)
    l_array = np.array(l_img,dtype=np.float64)
    y ,x = r_img.shape[:2]
    score = np.empty((x ,y))
    pos = np.zeros((y,x))
    return r_array,l_array,pos


def template_match(key):
    print("__start_template_match__")
    t1 = time.time()
    if key == 0:
        pos = sad_match()
    elif key == 1:
        pos = zncc_match()
    else:
        print("__false_keyward__")
        exit()
    t2 = time.time() -t1
    print("__Finish_time:{0}s__".format(t2))


    from PIL import Image

    Image.fromarray(np.uint8(pos)).save("stereo_gray.png")
    with open("stereo_match.txt","w") as f:
        f.write(pos)




def main(key):
    if key == "SAD":
        print("___SAD_match___")
        template_match(0)
    elif key == "ZNCC":
        print("___ZNCC_match___")
        template_match(1)
    else:
        print("__False_keyward__")
        exit()

    


if __name__=="__main__":
    if len(sys.argv) == 1:
        print("no imput key")
        exit()
    main(sys.argv[1])
        


