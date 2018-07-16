import numpy as np
import cv2
import random
import PIL as Image
def Ransac(pn):
    acc = []
    old = 0
    step =100
    number = pn.shape[0]
    for n in range(step):
        save = []
        print("__{0}step__".format(n))
        random_pick = [random.randint(0,number) for i in range(4)]
        print(random_pick)

        A = np.zeros((8,8))
        b = np.zeros(8)
        for i,k in enumerate(random_pick):
            i= i*2
            t = pn[k]
            A[i] = [t[0],t[1],1,0,0,0,-t[0]*t[2],-t[2]*t[1]]
            A[i+1] = [0,0,0,t[0],t[1],1,-t[0]*t[1],-t[1]**2]
            b[i] = t[2]
            b[i+1] = t[1]

        A_out = np.dot(A.T,A)
        A_out = np.linalg.inv(A_out)
        h = np.dot(A_out,A.T)
        h = np.dot(h,b.T)
        par = 0
        for t in pn:
            x = t[0]*h[0] + t[1]*h[1] + h[2] -t[0]*t[1]*h[6] - t[2]*t[1]*h[7]
            y = t[0]*h[3] + t[1]*h[4] + h[5] -t[0]*t[1]*h[6] - t[1]**2*h[7]

            d = (x-t[2])**2 + (y - t[1])**2
            if d < 2000:
                par +=1
                save.append(t)
        if par > old:
            acc = save
            old = par
        print(par)
    return acc, old

def random_sampling():
    img = np.load("stereo_match.npy")
    h,w = img.shape[:2]
    img2 = np.copy(img)
    print(h,w)
    pnt1 = []
    pnt2 = []
    pnt = []
    acc = []
    old = 0
    step =10
    for i in range(h):
        for j in range(w):
            if img[i,j]==0:
                continue
            dist = img[i,j]
            pnt1.append((j,i))
            pnt2.append((j+dist,i))
            pnt.append((j,i,j+dist))

    pnt1 = np.float32(pnt1)
    pnt2 = np.float32(pnt2)
    pn = np.array(pnt)
    print(pn.shape[0])
    acc,old= Ransac(pn)
    pn = np.array(acc)
    print("__2nd__")
    acc,old= Ransac(pn)
    print(old)
    img = np.zeros((480,640))
    for temp in acc:
        img[int(temp[1]),int(temp[0])] = temp[2] - temp[0]
    np.save("test1",img)

def main():
    random_sampling()

if __name__=="__main__":
    main()
