import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=['train']

classes = ["0"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):  # 转换这一张图片的坐标表示方式（格式）,即读取xml文件的内容，计算后存放在txt文件中。
    in_file = open('annotation/%s'% image_id)
    image_id=image_id.split('.')[0]
    out_file = open('labels/%s.txt'%image_id, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

for image_set in sets:
    if not os.path.exists('labels/'):
        os.makedirs('labels/')  # 新建一个 label 文件夹，用于存放yolo格式的标签文件：000001.txt
    image_ids = open('%s.txt' % image_set).read().strip().split()# 读取txt文件中 存放的图片的 id：000001
    for image_id in image_ids:
        image_id=image_id.split('/')[-1]
        image_id=image_id.split('.')[0]
        image_id=image_id+".xml"
        convert_annotation(image_id)  # 转换这一张图片的坐标表示方式（格式）


