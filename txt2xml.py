import os
import xml.etree.ElementTree as ET
from PIL import Image


def create_xml_annotation(image_path, labels_path, output_folder):
    # 读取图像尺寸
    image = Image.open(image_path)
    image_width, image_height = image.size

    # 创建XML根元素
    root = ET.Element('annotation')

    # 添加文件名元素
    filename_elem = ET.SubElement(root, 'filename')
    filename_elem.text = os.path.basename(image_path)

    # 添加图像尺寸元素
    size_elem = ET.SubElement(root, 'size')
    width_elem = ET.SubElement(size_elem, 'width')
    width_elem.text = str(image_width)
    height_elem = ET.SubElement(size_elem, 'height')
    height_elem.text = str(image_height)

    # 读取并转换每个目标的标注信息
    with open(labels_path, 'r') as f:
        for line in f:
            line = line.strip().split()
            class_id = line[0]
            center_x = float(line[1])
            center_y = float(line[2])
            width = float(line[3])
            height = float(line[4])

            # 计算边界框坐标
            xmin = int((center_x - width / 2) * image_width)
            ymin = int((center_y - height / 2) * image_height)
            xmax = int((center_x + width / 2) * image_width)
            ymax = int((center_y + height / 2) * image_height)

            # 添加目标元素
            object_elem = ET.SubElement(root, 'object')
            name_elem = ET.SubElement(object_elem, 'name')
            name_elem.text = class_id
            bndbox_elem = ET.SubElement(object_elem, 'bndbox')
            xmin_elem = ET.SubElement(bndbox_elem, 'xmin')
            xmin_elem.text = str(xmin)
            ymin_elem = ET.SubElement(bndbox_elem, 'ymin')
            ymin_elem.text = str(ymin)
            xmax_elem = ET.SubElement(bndbox_elem, 'xmax')
            xmax_elem.text = str(xmax)
            ymax_elem = ET.SubElement(bndbox_elem, 'ymax')
            ymax_elem.text = str(ymax)

    # 创建XML树并保存为文件
    xml_tree = ET.ElementTree(root)
    xml_filename = os.path.splitext(os.path.basename(image_path))[0] + '.xml'
    xml_path = os.path.join(output_folder, xml_filename)
    xml_tree.write(xml_path)


# 设置YOLO标注文件的文件夹路径
labels_folder = ""

# 设置图像文件夹路径
image_folder = ""

# 设置输出XML标注文件的文件夹路径
output_folder = ""

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 遍历每个YOLO标注文件
for filename in os.listdir(labels_folder):
    if filename.endswith('.txt'):
        image_filename = os.path.splitext(filename)[0] + '.png'
        image_path = os.path.join(image_folder, image_filename)
        labels_path = os.path.join(labels_folder, filename)
        create_xml_annotation(image_path, labels_path, output_folder)

print("转换完成！")
