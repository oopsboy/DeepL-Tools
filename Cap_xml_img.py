'''
    截图xml标签内容
'''

import sys
import os
from xml.etree import ElementTree as ET
# import cv2
from PIL import Image

Img_path = r'./JPEGImages'  # 图片保存目录
save_path = r'./output'  # 可视化后图片保存目录
xml_path = r'./Annotations'  # xml文件保存目录


def cut(file, file_cls):
    imgname = file_cls.replace('.xml', '.jpg')
    print(imgname)
    # print (file)
    file_id = os.path.join(file, file_cls)
    tree = ET.parse(os.path.join(xml_path, file_id))
    for obj in tree.iter('object'):
        bbox = obj.find('bndbox')
        # Make pixel indexes 0-based
        x1 = int(bbox.find('xmin').text)
        y1 = int(bbox.find('ymin').text)
        x2 = int(bbox.find('xmax').text)
        y2 = int(bbox.find('ymax').text)
        cls = obj.find('name').text.strip()
        img = Image.open(os.path.join(Img_path, file, imgname))
        # print(img)
        cropped = img.crop((x1, y1, x2, y2))  # 切片  用来街截取图片
        imagename = cls + imgname
        isExists = os.path.exists(os.path.join(save_path, cls))
        if not isExists:
            os.makedirs(os.path.join(save_path, cls))
        x, y = cropped.size
        if x >= 300 or y >= 300:
            cropped.save(os.path.join(save_path, cls, imagename), quality=95)  # 保存图片没有损失


if __name__ == '__main__':
    b = 0
    file_name = os.listdir(xml_path)
    for file in file_name:
        for file_cls in os.listdir(os.path.join(xml_path, file)):
            print(file_cls)
            cut(file, file_cls)
    b = b + 1
    print(b)
