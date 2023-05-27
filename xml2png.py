import cv2
import os
import os.path
import xml.etree.cElementTree as ET

def draw(image_path, xml_path, root_saved_path):
    "图片根据标注画框"
    src_img_path = image_path
    src_ann_path = xml_path
    for file in os.listdir(src_ann_path):
        file_name, suffix = os.path.splitext(file)
        if suffix == '.xml':
            xml_path = os.path.join(src_ann_path,file)
            image_path = os.path.join(src_img_path,file_name+'.png')
            img = cv2.imread(image_path)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            for obj in root.iter('object'):
                name = obj.find('name').text
                xml_box = obj.find('bndbox')
                x1 = int(xml_box.find('xmin').text)
                x2 = int(xml_box.find('xmax').text)
                y1 = int(xml_box.find('ymin').text)
                y2 = int(xml_box.find('ymax').text)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), thickness=2)
                cv2.putText(img, name, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), thickness=2)
            cv2.imwrite(os.path.join(root_saved_path, file_name+'.jpg'), img)


if __name__ == '__main__':
    image_path = r'./images'
    xml_path = r'./xml'
    root_save_path = r'./tt'
    draw(image_path, xml_path, root_save_path)