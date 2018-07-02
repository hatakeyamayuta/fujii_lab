import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2


def plot_3d():
    x = []
    y = []
    z = []
    x.append(1)
    y.append(1)
    z.append(1)
    img = cv2.imread("gray.png",0)
    cv2.imshow("stereo",img)
    #img *=255
    kernel = np.ones((5,5),np.uint8)
    mor = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
    mor = cv2.morphologyEx(mor,cv2.MORPH_OPEN,kernel)
    cv2.imshow("mor",mor)
    cv2.waitKey(0)
    h, w = img.shape[:2]
    img_array = np.array(mor,dtype=np.float32)
    for i in range(0,h):
        for j in range(0,w):
            if img_array[i][j] == 0:
                continue
            if img_array[i][j] > 180:
                t_z = (663*262)/img_array[i][j]
                t_x = (328-j)*t_z/663
                t_y = (i-245)*t_z/661

                y.append(t_x)
                x.append(t_y)
                z.append(t_z)

    fig = plt.figure()
    print("x={0}".format(len(x)))
    print("x={0}".format(len(y)))
    print("x={0}".format(len(z)))
    ax = Axes3D(fig)
    ax.plot(x,y,z,"o",color="#00cccc",ms=0.4,mew=0.5)
    #ax.scatter3D(x,y,z)

    ax.set_xlabel("y")
    ax.set_ylabel("x")
    ax.set_zlabel("z")
    plt.show()
    return
plot_3d()
