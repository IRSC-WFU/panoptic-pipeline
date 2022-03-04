import numpy as np
import cv2
import os
import argparse
from PIL import Image
import numpy
import sys


if __name__ == '__main__':

    
    top_dir = "/deac/generalGrp/paucaGrp/dark_mining/panoptic-pipeline"
    img_folder = os.path.join(top_dir, "images/images")
    anno_folder = os.path.join(top_dir, "images/annotations")
 
    
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    
    new_img_folder = os.path.join(top_dir, 'images-t-' + sys.argv[1] + "_" + sys.argv[2] + "/images")
    new_ano_folder = os.path.join(top_dir, 'images-t-' + sys.argv[1] + "_" + sys.argv[2] + "/annotations")
    if not os.path.exists(new_img_folder):
        os.makedirs(new_img_folder)
    
    if not os.path.exists(new_ano_folder):
        os.makedirs(new_ano_folder)

    for filename in os.listdir(img_folder):
        img = Image.open(os.path.join(img_folder,filename))
        x_num = int(img.size[0] / x)
        y_num = int(img.size[1] / y)
        count = 0
        for i in range (1, x_num + 1):
            for j in range (1, y_num + 1):
                left = (j-1)*x
                right = j*x
                top = (i-1)*y
                bottom = i*y
                
                new_image = img.crop((left, top, right, bottom))
                name = os.path.splitext(os.path.basename(filename))
                new_image.save(os.path.join(new_img_folder, name[0] + "-t-" + str(count) + ".jpg"))
                count += 1
        print("Tiling image: ", filename)
    
    for filename in os.listdir(anno_folder):
        img = Image.open(os.path.join(anno_folder,filename))
        x_num = int(img.size[0] / x)
        y_num = int(img.size[1] / y)
        count = 0
        for i in range (1, x_num + 1):
            for j in range (1, y_num + 1):
                left = (j-1)*x
                right = j*x
                top = (i-1)*y
                bottom = i*y
                new_image = img.crop((left, top, right, bottom))
                name = os.path.splitext(os.path.basename(filename))
                imgname = name[0].split('_')
                imgname[0] = imgname[0] + "-t-" + str(count)
                imgname = "_".join(imgname)
                new_image.save(os.path.join(new_ano_folder, imgname + ".png"))
                count += 1
    print("Tiling annotation: ", filename)
    