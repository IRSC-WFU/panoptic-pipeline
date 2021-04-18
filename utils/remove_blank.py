import argparse
import os
import fnmatch
import re
import json

import multiprocessing

import numpy as np
from PIL import Image

def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg', '*.png', '*.tif', '*.TIF']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    
    return files

def filter_for_annotations(root, files, image_filename):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension + '.*'
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]

    return files

def isCategory(filename, categories):
    file_cat = filename.split('_')[-2]
    if file_cat in categories:
        return True
    return False

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-d","--directory",dest="directory",help="Directory Name", default='images')
    parse.add_argument("-t","--threshold",dest="thr",help="Threshold Percentage", type=float, default=0.02)
    parse.add_argument("-c","--categories",dest="categories",help="Categories JSON File", default='panoptic_coco_categories.json')
    parse.add_argument("-r","--remove",dest="rm",help="Remove Blank Images?", default=False)
    args = parse.parse_args()

    with open(args.categories, 'r') as f:
        CATEGORIES = [i['name'] for i in json.load(f)]

    def process_image(curr):
        annotations = filter_for_annotations(os.path.join(args.directory, 'annotations'), os.listdir(os.path.join(args.directory, 'annotations')), curr)
        
        with Image.open(os.path.join(args.directory, 'images', curr)) as img:
            background = np.zeros(img.size)
        
        file_list = [os.path.join(args.directory, 'images', curr)]

        for i in annotations:
            file_list.append(i)
            if isCategory(i, CATEGORIES):
                background+= np.array(Image.open(i).convert('1')).astype(np.uint8)
        
        if background.sum() <= background.shape[0]*background.shape[1]*args.thr:
            if args.rm:
                for i in file_list:
                    os.remove(i)
            else:
                for i in file_list:
                    print(i)

    pool = multiprocessing.Pool(4) 

    jobs = []

    for curr in filter_for_jpeg(os.path.join(args.directory, 'images'), os.listdir(os.path.join(args.directory, 'images'))):
        p = multiprocessing.Process(target=process_image, args=[os.path.basename(curr)])
        jobs.append(p)
        p.start()

    
    for proc in jobs:
        proc.join()
