import numpy as np
import cv2
import os
import argparse
from PIL import Image
import numpy
import sys



if __name__ == '__main__':

    
    top_dir = "/deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining"
    img_folder = os.path.join(top_dir, "images/images")
    anno_folder = os.path.join(top_dir, "images/annotations")
 
    
    scale = float(sys.argv[1])
    print(scale)
    
    new_img_folder = os.path.join(top_dir, 'images-d-' + str(scale) + "/images")
    new_ano_folder = os.path.join(top_dir, 'images-d-' + str(scale) + "/annotations")
    if not os.path.exists(new_img_folder):
        os.makedirs(new_img_folder)
    
    if not os.path.exists(new_ano_folder):
        os.makedirs(new_ano_folder)

    for filename in os.listdir(img_folder):
        img = Image.open(os.path.join(img_folder,filename))
        x = int(img.size[0] * scale)
        y = int(img.size[1] * scale)
        new_image = img.resize((x, y))
        name = os.path.splitext(os.path.basename(filename))
        new_image.save(os.path.join(new_img_folder, name[0] + "-d-" + str(scale) + ".jpg"))
        print("DownSampling: ", filename)
        
    
    for filename in os.listdir(anno_folder):
        img = Image.open(os.path.join(anno_folder,filename))
        x = int(img.size[0] * scale)
        y = int(img.size[1] * scale)
        new_image = img.resize((x, y))
        name = os.path.splitext(os.path.basename(filename))
        imgname = name[0].split('_')
        imgname[0] = imgname[0] + "-d-" + str(scale)
        imgname = "_".join(imgname)
        new_image.save(os.path.join(new_ano_folder, imgname + ".png"))
        print("DownSampling: ", filename)
        
        

    