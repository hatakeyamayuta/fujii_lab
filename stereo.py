import cv2
import numpy as np
import configparser
from cari import carib
class stereo():

    def __init__(self):
        config = configparser.ConfigParser()
        try:
            config.read("camera_config.ini","UTF-8")
            camera = config["SET"]

            self.right_impath = camera.get("right_path")
            self.left_impath = camera.get("left_path")
            self.forcus = camera.getfloat("forcus")
            self.distance = camera.getfloat("distance")
            self.pix = camera.getfloat("pix")
        except:
            print("Read Error")
            exit()

    def get_ball_pos(self,img):
        img = carib(img)
        img = cv2.bilateralFilter(img,9,70,70)#シャープ化
        img = cv2.medianBlur(img,5)#平均フィルタ
        cmg = cv2.Canny(img,90,180)
        try:
            circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,40,50,param1=130,param2=120,minRadius=5,maxRadius=300)
            circles = np.around(circles)
            circles = np.array(circles,dtype='uint16')

            for i in circles[0,:]:

                cv2.circle(cmg,(i[0],i[1]),i[2],(255,255,255),2)
                cv2.circle(cmg,(i[0],i[1]),2,(0,0,255),3)

                print(i)
        except:
            print("NOT FIND")
        i[0] = i[0] - 420
        i[1] = 240 - i[1]
        cv2.imshow('tes',cmg)
        cv2.waitKey(0)
        return i

    def predict_pos(self,r_pos,l_pos):

        d = r_pos[0] - l_pos[0]
        Z = (self.distance*self.forcus)/(d*self.pix)
        Y = r_pos[1]*Z/self.forcus
        X = r_pos[0]*Z/self.forcus
        return (X,Y,Z)


    def test(self):
        print(self.pix)
        r_img = cv2.imread(self.right_impath,0)
        l_img = cv2.imread(self.left_impath,0)

        r_pos = self.get_ball_pos(r_img)
        print(r_pos)
        l_pos = self.get_ball_pos(l_img)
        
        print(self.predict_pos(r_pos,l_pos))
    



        
t = stereo()
t.test()
