import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
x = []
y = []
z = []
def plot_3d():
    img = cv2.imread("gray.png",0)
    h, w = img.shape[:2]
    img_array = np.array(img)
    for i in range(0,h):
        for j in range(0,w):
            if img_array[i][j] == 0:
                continue

            t_z = (494*500)/img_array[i][j]/16
            t_x = (330-j)*t_z/494
            t_y = (i-190)*t_z/494

            x.append(t_x)
            y.append(t_y)
            z.append(t_z)

def main():
    #x = np.random.randn(100)
    #y = np.random.randn(100)
    #z = np.random.randn(100)
    #set_camera_position

    x.append(0)
    y.append(0)
    z.append(0)

    plot_3d()
    fig = plt.figure()
    print("x={0}".format(len(x)))
    print("x={0}".format(len(y)))
    print("x={0}".format(len(z)))
    ax = Axes3D(fig)
    ax.plot(x,y,z,"o",color="#00aa01",ms=1,mew=0.5)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.show()

if __name__=="__main__":
    main()
