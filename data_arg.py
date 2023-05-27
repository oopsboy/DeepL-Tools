from PIL import Image
from glob import glob
import xml.etree.ElementTree as ET
import os
import albumentations as A
import cv2
import numpy as np
import pdb

imgs_dir = 'E:\\BaiduNetdiskDownload\\dataset\\DTdata\\val\\images'
labels_dir = 'E:\\BaiduNetdiskDownload\\dataset\\DTdata\\val\\xml'
images_save_dir = 'E:\\BaiduNetdiskDownload\\dataset\\aug\\val\\images'
anno_save_dir = 'E:\\BaiduNetdiskDownload\\dataset\\aug\\val\\xml'
rates = [90, 180, 270]


def UpdateTree(tree, path, w):
    root = tree.getroot()
    root.findall('filename')[0].text = path.replace('xml', 'png')
    for obj in root.findall('object'):
        xmin = int(obj.findall('bndbox')[0].findall('xmin')[0].text)
        ymin = int(obj.findall('bndbox')[0].findall('ymin')[0].text)
        xmax = int(obj.findall('bndbox')[0].findall('xmax')[0].text)
        ymax = int(obj.findall('bndbox')[0].findall('ymax')[0].text)
        obj.findall('bndbox')[0].findall('xmin')[0].text = str(w - xmax)
        obj.findall('bndbox')[0].findall('xmax')[0].text = str(w - xmin)
    tree.write(anno_save_dir + '/' + path)


def UpdateName(tree, filename, path):
    root = tree.getroot()
    root.findall('filename')[0].text = filename
    tree.write(anno_save_dir + '/' + path)


def UpdateXml(img, path):
    # pdb.set_trace()
    h, w = img.shape[0], img.shape[1]
    # 读取xml文件，以树的结构存储
    tree = ET.parse(labels_dir + '/' + path.replace('png', 'xml'))
    # 原图的anno
    UpdateName(tree, path.replace('png', 'png'), path.replace('.png', '.xml'))
    # random contrast 的anno
    UpdateName(tree, path.replace('.png', '_rc.png'), path.replace('.png', '_rc.xml'))
    # random brightness的anno
    UpdateName(tree, path.replace('.png', '_rb.png'), path.replace('.png', '_rb.xml'))
    # blur的anno
    UpdateName(tree, path.replace('.png', '_blur.png'), path.replace('.png', '_blur.xml'))
    # mb的anno
    UpdateName(tree, path.replace('.png', '_mb.png'), path.replace('.png', '_mb.xml'))
    # random gamma的anno
    UpdateName(tree, path.replace('.png', '_rg.png'), path.replace('.png', '_rg.xml'))
    # clahe的anno
    UpdateName(tree, path.replace('.png', '_clahe.png'), path.replace('.png', '_clahe.xml'))
    # 水平翻转
    UpdateTree(tree, path.replace('.png', '_h.xml'), w)
    # 重新读取xml文件，刚刚翻转已经更改了数值
    tree = ET.parse(labels_dir + '/' + path.replace('png', 'xml'))
    name = ''

    # 旋转
    for rate in rates:
        num = 0
        obj_num = 0
        tree = ET.parse(labels_dir + '/' + path.replace('png', 'xml'))
        print(rate, w, h)
        root = tree.getroot()
        h_new = int((w - h) / 2)  # 多出的部分的一半
        for obj in root.findall('object'):
            obj_num += 1
            xmin = int(obj.findall('bndbox')[0].findall('xmin')[0].text)
            ymin = int(obj.findall('bndbox')[0].findall('ymin')[0].text)
            xmax = int(obj.findall('bndbox')[0].findall('xmax')[0].text)
            ymax = int(obj.findall('bndbox')[0].findall('ymax')[0].text)
            # pdb.set_trace()
            if rate == rates[0]:
                x1 = ymin
                y1 = w - xmax
                x2 = ymax
                y2 = w - xmin
                name = '_90.xml'

            elif rate == rates[1]:
                x1 = w - xmax
                y1 = h - ymax
                x2 = w - xmin
                y2 = h - ymin
                name = '_180.xml'

            elif rate == rates[2]:
                x2 = h - ymin
                y2 = xmax
                x1 = h - ymax
                y1 = xmin
                name = '_270.xml'

            y = y1 + int((y2 - y1) / 2)
            # 判断box的中心点y坐标是否在图片内，在则保留
            y_new = y1 + int((y2 - y1) / 2)  # 旋转之后的box的中心点y坐标
            if rate == rates[1]:
                obj.findall('bndbox')[0].findall('xmin')[0].text = str(x1)
                obj.findall('bndbox')[0].findall('ymin')[0].text = str(y1)
                obj.findall('bndbox')[0].findall('xmax')[0].text = str(x2)
                obj.findall('bndbox')[0].findall('ymax')[0].text = str(y2)
            else:
                if y <= w - h_new and y >= h_new:
                    obj.findall('bndbox')[0].findall('xmin')[0].text = str(x1 + h_new)
                    obj.findall('bndbox')[0].findall('ymin')[0].text = str(y1 - h_new)
                    obj.findall('bndbox')[0].findall('xmax')[0].text = str(x2 + h_new)
                    obj.findall('bndbox')[0].findall('ymax')[0].text = str(y2 - h_new)
                else:
                    num += 1
                    # print('当前rota:',rate,'This box should be removed!')
                    root.remove(obj)
        root.findall('filename')[0].text = path.replace('.png', name).replace('xml', 'png')
        tree.write(os.path.join(anno_save_dir, path.replace('.png', name)))
        print(path, rate, '共计', obj_num, '个box,', '总计删除了', num, '个box!')


def Aug(aug, img, path):
    result = aug(image=img)["image"]
    cv2.imwrite(os.path.join(images_save_dir, path), cv2.cvtColor(result, cv2.COLOR_BGR2RGB))


def RotateImg(im2, rota, path):
    rot = im2.rotate(rota, expand=0)
    # 创建一个与旋转图像大小相同的白色图像
    fff = Image.new('RGBA', rot.size, (192,) * 4)
    # 使用alpha层的rot作为掩码创建一个复合图像
    out = Image.composite(rot, fff, rot)
    # 保存
    out.convert(im2.mode).save(os.path.join(images_save_dir, path))


if __name__ == "__main__":
    imgs_list = os.listdir(imgs_dir)

    for path in imgs_list:
        print('开始处理图片:', path, '......')
        # pdb.set_trace()
        img = cv2.imread(os.path.join(imgs_dir, path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(images_save_dir, path.replace('png', 'png')), cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        Aug(A.Blur(), img, path.replace('.png', '_blur.png'))
        Aug(A.CLAHE(), img, path.replace('.png', '_clahe.png'))
        Aug(A.MedianBlur(), img, path.replace('.png', '_mb.png'))
        Aug(A.GaussianBlur(), img, path.replace('.png', '_rb.png'))
        Aug(A.RandomBrightnessContrast(), img, path.replace('.png', '_rc.png'))
        Aug(A.RandomGamma(), img, path.replace('.png', '_rg.png'))
        Aug(A.HorizontalFlip(p=1), img, path.replace('.png', '_h.png'))
        img = Image.fromarray(img).convert("RGBA")
        RotateImg(img, 90, os.path.join(images_save_dir, path.replace('.png', '_90.png')))
        RotateImg(img, 180, os.path.join(images_save_dir, path.replace('.png', '_180.png')))
        RotateImg(img, 270, os.path.join(images_save_dir, path.replace('.png', '_270.png')))
        print('开始处理xml文件', path)
        UpdateXml(np.array(img), path)
