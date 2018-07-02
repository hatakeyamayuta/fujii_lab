import numpy as np
import cv2

def ransac():
    img = cv2.imread("stereo_gray2.png",0)
    w,h = img.shape[:2]
    print(h,w)
    pnt1 = []
    pnt2 = []
    for i in range(h):
        for j in range(w):
            if img[j,i]==0:
                continue
            dist = img[j,i]
            pnt1.append((i,j))
            pnt2.append((i,j+dist))
            img[j,i] = 0
    pnt1 = np.float32(pnt1)
    pnt2 = np.float32(pnt2)
    print(pnt1)
    print(pnt2)
    F, mask = cv2.findFundamentalMat(pnt1,pnt2,cv2.LMEDS)
    print(mask)

    print(pnt1.shape)
    pnt1 = pnt1[mask.ravel()==1]
    pnt2 = pnt2[mask.ravel()==1]
    print(pnt1.shape)                                   
    for k,pt in enumerate(pnt1):
        i,j = map(int,pt)
        img[j,i] = pnt2[k,1] - i
    cv2.imshow("test",img)
    cv2.waitKey(0)
def main():

    ransac()


if __name__=="__main__":
    main()
