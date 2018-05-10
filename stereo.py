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
            self.fx = camera.getfloat("fx")
            self.fy = camera.getfloat("fy")
            self.cx = camera.getfloat("cx")
            self.cy = camera.getfloat("cy")
            self.distance = camera.getfloat("distance")
            self.pix = camera.getfloat("pix")
        except:
            print("__Read Error__")
            exit()

    def get_ball_pos(self,img):
        #img = carib(img)
        img = cv2.bilateralFilter(img,9,70,70)#シャープ化
        img = cv2.medianBlur(img,5)#平均フィルタ
        cmg = cv2.Canny(img,90,180)
        try:
            circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,400,param1=100,param2=35,minRadius=22,maxRadius=50)
            circles = np.around(circles)
            circles = np.array(circles,dtype='uint16')

            for i in circles[0,:]:

                cv2.circle(img,(i[0],i[1]),i[2],(255,255,255),2)
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

                print(i)
                break
        except:
            print("__NOT FIND CIRCLE__")
            exit()

        cv2.imshow('tes',img)
        cv2.waitKey(0)
        return i

    def predict_pos(self,r_pos,l_pos):

        d = (r_pos[0] - l_pos[0])
        #d = 242
        print("d={0}".format(d))
        Z = (self.distance*self.fx)/d
        Y = (self.cy-r_pos[1])*Z/self.fy
        X = (r_pos[0]-self.cx)*Z/self.fx

        return (X,Y,Z)


    def test(self):
        print(self.pix)
        r_img = cv2.imread(self.right_impath,0)
        l_img = cv2.imread(self.left_impath,0)
        
        r_pos = self.get_ball_pos(r_img)
        l_pos = self.get_ball_pos(l_img)
        #r_pos = [406,150-316]
        #l_pos = [320,318]
        print(self.predict_pos(r_pos,l_pos))
        print("acc{0}".format(np.sqrt(1200**2+74**2)))



if __name__=="__main__":

    t = stereo()
    t.test()
