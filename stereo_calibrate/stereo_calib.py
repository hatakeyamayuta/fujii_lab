import numpy as np
import cv2

def get_camera_param():
    #camera_paramerter
    K_left = np.array([[663.42,    0,3.282e+02],
                       [    0,6.61e+02,2.425e+02],
                       [    0,    0,    1]])

    K_right = np.array([[661.5,    0,302.6],
                        [    0,660.9,255.8],
                        [    0,    0,    1]])


    dist_left = np.array([-0.0789,0.023,0,0])
    dist_right = np.array([-0.0349,-0.249,0,0])

    R_left = np.array([[1,0,0],
                       [0,1,0],
                       [0,0,1]])
    
    R_right = np.array([[    0.9965,0.0031, 0.0832],
                       [-6.2822e-04,0.9996,-0.0294],
                       [    -0.0832,0.0293, 0.9961]])

    T_left = np.array([[0],
                       [0],
                       [0]])

    T_right = np.array([[-262.15],
                        [- 22.71],
                        [ -3.599]])
    return K_left,K_right,dist_left,dist_right,R_left,R_right,T_left,T_right


left_img = cv2.imread("left3.jpg",1)
right_img = cv2.imread("right3.jpg",1)

size = (640,480)

k_l,k_r,d_l,d_r,r_l,r_r,t_l,t_r = get_camera_param()

newcameramtx_l, roi=cv2.getOptimalNewCameraMatrix(k_l,d_l,(480,640),0,(480,640))
x,y,w,h = roi
dst_l = cv2.undistort(left_img, k_l, d_l, None, newcameramtx_l)
#dst_l = dst_l[y:y+h, x:x+w]
newcameramtx_r, roi=cv2.getOptimalNewCameraMatrix(k_r,d_r,(480,640),0,(480,640))
dst_r = cv2.undistort(right_img, k_r, d_r, None, newcameramtx_r)

R1, R2, P1, P2, Q,n1,n2 = cv2.stereoRectify(k_l,d_l,k_r,d_r,size,r_r,t_r,flags=cv2.CALIB_ZERO_DISPARITY,
                                                 alpha=0,newImageSize=size)

map1,map2 = cv2.initUndistortRectifyMap(k_l,d_l,R2,P1,size,cv2.CV_32FC1)
map_r1,map_r2 = cv2.initUndistortRectifyMap(k_r,d_r,R1,P2,size,cv2.CV_32FC1)

left_dst = cv2.remap(left_img,map1,map2,cv2.INTER_LINEAR)
right_dst = cv2.remap(right_img,map_r1,map_r2,cv2.INTER_LINEAR)
print(P2)
cv2.imshow("test_l",left_dst)
cv2.imshow("test_r",right_dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("stereo_calib_left.png",left_dst)
cv2.imwrite("stereo_calib_right.png",right_dst)


