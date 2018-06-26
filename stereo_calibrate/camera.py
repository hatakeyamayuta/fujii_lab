import cv2
import subprocess
cap = cv2.VideoCapture(0)
cmd='v4l2-ctl -d /dev/video0 -c exposure_auto=3' # 自動露出
ret = subprocess.check_output([cmd],shell=True)
# 設定した後にすぐ変更するとうまく反映されないので、10回程度ムダにカメラ回す
_ = [cap.read()[:1] for h in range(10)]
cmd = 'v4l2-ctl -d /dev/video0 -c exposure_auto=1' # 現状で露出固定
ret = subprocess.check_output([cmd],shell=True)
