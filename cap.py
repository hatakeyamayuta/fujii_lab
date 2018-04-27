import cv2
import numpy as np
img_path_r ='r_image.png'

img_path_l ='l_image.png'
if __name__=="__main__":
    r_capture = cv2.VideoCapture(0)
    l_capture = cv2.VideoCapture(1)

    if r_capture.isOpened() is False:
        print("IO Error")

    cv2.namedWindow("r_Capture", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("l_Capture", cv2.WINDOW_AUTOSIZE)
    while True:

        r_ret, r_image = r_capture.read()

        l_ret, l_image = l_capture.read()
        if r_ret == False:
            continue

        cv2.imshow("r_Capture", r_image)

        cv2.imshow("l_Capture", l_image)
        k = cv2.waitKey(1)
        if k == 27:
            cv2.imwrite("r_image.png", r_image)
            cv2.imwrite("l_image.png", l_image)
            print("""""write_image""""")
        if k == 42:
            break

    cv2.destroyAllWindows()

