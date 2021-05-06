import os
from PIL import Image
import argparse


def txt2xml(image_list, classes_file):
    classes = open(classes_file).read().splitlines()
    print("classes ", classes)
    with open(image_list, "r") as file:
        files = file.readlines()
    for file in files:
        img_path = file.strip()
        img_file = Image.open(img_path)
        txt_path = img_path.replace('.jpg', '.txt').replace('images', 'labels')
        print("txt_path ", txt_path)
        txt_file = open(txt_path).read().splitlines()
        xml_path = txt_path.replace('.txt', '.xml').replace('labels', 'annotation')
        save_xml_root = os.path.dirname(xml_path)
        print(save_xml_root)
        if not os.path.exists(save_xml_root):
            os.makedirs(save_xml_root)
        xml_file = open(xml_path, 'w')
        width, height = img_file.size
        xml_file.write('<annotation>\n')
        xml_file.write('\t<folder>simple</folder>\n')
        xml_file.write('\t<filename>' + str(os.path.basename(img_path)) + '</filename>\n')
        xml_file.write('\t<path>' + str(img_path) + '</path>\n')
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
        xml_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--classes_file", type=str, default="")
    parser.add_argument('--image_list', type=str, default="")
    opt = parser.parse_args()
    txt2xml(opt.image_list, opt.classes_file)