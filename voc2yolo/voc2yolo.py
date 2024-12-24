"""
├── voc2yolo.py
└── VOCdevkit
    └── VOC2007
        ├── Annotations
        ├── ImageSets
        └── JPEGImages
Annotations: 用来存放xml格式的标注文件
JPEGImages: 用来存放图片数据集
ImageSets: 数据集划分文件，类别标签，图片名称list的txt文件

├── yolo_output.md
└── VOC2007
    ├── images
    └── labels
功能： 将voc格式的标签转换成yolo格式，并且同步拷贝图像
"""

import argparse
import os
import shutil
import xml.etree.ElementTree as ET

classes = ["aeroplane", 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog',
           'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']  # class names


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(anno_path, image_path, save_label_path, save_image_path):
    in_file = open(anno_path, 'r')
    out_file = open(save_label_path, 'w')

    tree = ET.parse(in_file)
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
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    # 需要把图片拷贝到相应的文件夹
    shutil.copy(image_path, save_image_path)
    in_file.close()
    out_file.close()


if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--root_path', type=str, default='VOCdevkit/VOC2007', help='Directory path')
    argparse.add_argument('--output_dir', type=str, default='yolo_output', help='Output directory')
    args = argparse.parse_args()

    anno_paths = os.path.join(args.root_path, 'Annotations')
    image_paths = os.path.join(args.root_path, 'JPEGImages')
    if not os.path.exists(anno_paths) or not os.path.exists(image_paths):
        print("NOT FOUND Annotations or JPEGImages")
        exit(1)

    # 输出文件夹标签路径
    output_labels_paths = os.path.join(args.output_dir, 'labels')
    # 输出文件夹图像路径
    output_images_paths = os.path.join(args.output_dir, 'images')
    if not os.path.exists(output_labels_paths):
        os.makedirs(output_labels_paths)
    if not os.path.exists(output_images_paths):
        os.makedirs(output_images_paths)

    # ImageSets如果存在
    if os.path.exists(os.path.join(args.root_path, 'ImageSets/Main/train.txt')):
        with open(os.path.join(args.root_path, 'ImageSets/Main/train.txt'), 'r') as f:
            voc_file_list = [r.strip() for r in f.readlines()]
    else:
        image_lists = os.listdir(image_paths)
        for image_name in image_lists:
            image_path = os.path.join(image_paths, image_name)
            basename_no_ext = os.path.splitext(image_name)[0]
            if not os.path.exists(os.path.join(anno_paths, basename_no_ext + '.xml')):
                continue
            anno_path = os.path.join(anno_paths, basename_no_ext + '.xml')
            save_label_path = os.path.join(output_labels_paths, basename_no_ext + '.txt')
            save_image_path = os.path.join(output_images_paths, basename_no_ext + '.jpg')

            convert_annotation(anno_path, image_path, save_label_path, save_image_path)
    print("Finished processing: ", args.root_path)
