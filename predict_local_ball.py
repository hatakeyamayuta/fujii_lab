import cv2
import numpy as np

rb_path = "right_ball.png"
lb_path = "left_ball.png"

r_img = cv2.imread(rb_path)

l_img = cv2.imread(lb_path)


def predict_local():
    #CAM_range
    b = 100 

    #CMOS wide height(mm)
    c_w, c_h = 23.4, 16.7
    
    #forcus_rage(mm)
    f = 18
    
    #img_size
    im_w, im_h = 640, 480

    #pixcel
    pi = np.sqrt((im_w*im_h)/(c_w*c_h))
    
    # resize 
    res_x, res_y = c_w/im_w, c_h/im_h

    r_x, r_y r_img= get_points(r_img)
    l_x, l_y l_img= get_points(l_img)
    
    
    Z = (f*b)/(pi*(r_x-l_y))
    X = Z/f*r_x
    Y = Z/f*r_y

def get_points(img):
    img = cv2.GaussianBlur(img,(5,5),0)
    img = cv2.bilateralFilter(img,9,70,70)
    img = cv2.medianBlur(img,5)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=180,param2=20,minRadius=5,maxRadius=80)
    circles = np.around(circles)
    circles = np.array(circles,dtype='uint16')

    for i in circles[0,:]:
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        print(i)
        break
    x = 340 - i[0]
    y = 240 - i[1] + i[2]

    return x, y, img

if __name__=="__main__":

    predict_local()

    

    
           


