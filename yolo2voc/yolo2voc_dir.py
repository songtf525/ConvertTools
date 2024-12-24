"""
├── yolo2voc.py
└── VOCdevkit
    └── VOC2007
        ├── Annotations
        ├── ImageSets
        └── JPEGImages
Annotations: 用来存放xml格式的标注文件
JPEGImages: 用来存放图片数据集
ImageSets: 数据集划分文件，类别标签，图片名称list的txt文件

功能: yolo格式数据集转换为voc格式，这个脚本输入图像路径，标签路径，类别名称和保存xml的路径
缺点: 如何yolo标签层级很深很复杂，使用路径输入可能就要操作多次，易出错，适用于全部图像和标签在一个文件夹的情形
"""
import argparse
import os

from PIL import Image


def txtLabel_to_xmlLabel(classes_file, source_txt_path, source_img_path, save_xml_path):
    if not os.path.exists(save_xml_path):
        os.makedirs(save_xml_path)
    classes = open(classes_file).read().splitlines()
    print(classes)
    for file in os.listdir(source_txt_path):
        img_path = os.path.join(source_img_path, file.replace('.txt', '.png'))
        img_file = Image.open(img_path)
        txt_file = open(os.path.join(source_txt_path, file)).read().splitlines()
        print(txt_file)
        xml_file = open(os.path.join(save_xml_path, file.replace('.txt', '.xml')), 'w')
        width, height = img_file.size
        xml_file.write('<annotation>\n')
        xml_file.write('\t<folder>simple</folder>\n')
        xml_file.write('\t<filename>' + str(file) + '</filename>\n')
        xml_file.write('\t<size>\n')
        xml_file.write('\t\t<width>' + str(width) + ' </width>\n')
        xml_file.write('\t\t<height>' + str(height) + '</height>\n')
        xml_file.write('\t\t<depth>' + str(3) + '</depth>\n')
        xml_file.write('\t</size>\n')

        for line in txt_file:
            print(line)
            line_split = line.split(' ')
            x_center = float(line_split[1])
            y_center = float(line_split[2])
            w = float(line_split[3])
            h = float(line_split[4])
            xmax = int((2 * x_center * width + w * width) / 2)
            xmin = int((2 * x_center * width - w * width) / 2)
            ymax = int((2 * y_center * height + h * height) / 2)
            ymin = int((2 * y_center * height - h * height) / 2)

            xml_file.write('\t<object>\n')
            xml_file.write('\t\t<name>' + str(classes[int(line_split[0])]) + '</name>\n')
            xml_file.write('\t\t<pose>Unspecified</pose>\n')
            xml_file.write('\t\t<truncated>0</truncated>\n')
            xml_file.write('\t\t<difficult>0</difficult>\n')
            xml_file.write('\t\t<bndbox>\n')
            xml_file.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
            xml_file.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')
            xml_file.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
            xml_file.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')
            xml_file.write('\t\t</bndbox>\n')
            xml_file.write('\t</object>\n')
        xml_file.write('</annotation>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--classes_file', type=str, default="person.names")
    parser.add_argument('--source_txt_path', type=str, default="")
    parser.add_argument('--source_img_path', type=str, default="")
    parser.add_argument('--save_xml_path', type=str, default="")
    opt = parser.parse_args()

    txtLabel_to_xmlLabel(opt.classes_file, opt.source_txt_path, opt.source_img_path, opt.save_xml_path)
