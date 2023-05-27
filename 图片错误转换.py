import os
import cv2

dataDir = "E:\\BaiduNetdiskDownload\\VOC2028\\VOC2028\\JPEGImages\\"
saveDir = "E:\\BaiduNetdiskDownload\\VOC2028\\VOC2028\\images\\"
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

for one_pic in os.listdir(dataDir):
    one_path = dataDir + one_pic
    one_img = cv2.imread(one_path)
    new_path = saveDir + one_pic
    cv2.imwrite(new_path, one_img)