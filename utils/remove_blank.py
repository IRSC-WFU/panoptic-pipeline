import argparse
import os
import fnmatch
import sys
import re
import json
import traceback
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
    parse.add_argument("-n","--non-zero",dest="nonzero",help="Only images with some labels", default=False)
    parse.add_argument("-c","--categories",dest="categories",help="Categories JSON File", default='panoptic_coco_categories.json')
    parse.add_argument("-r","--remove",dest="rm",help="Remove Blank Images?", default=False)
    args = parse.parse_args()

    with open(args.categories, 'r') as f:
        CATEGORIES = [i['name'] for i in json.load(f)]

    def process_image(curr):
        annotations = filter_for_annotations(os.path.join(args.directory, 'annotations'), os.listdir(os.path.join(args.directory, 'annotations')), curr)
        
        with Image.open(os.path.join(args.directory, 'images', curr)) as img:
            background = np.zeros((np.array(img).shape[0], np.array(img).shape[1]))
        
        file_list = [os.path.join(args.directory, 'images', curr)]
        blank_list = []
        for i in annotations:
            file_list.append(i)
            if isCategory(i, CATEGORIES):
                try:
                    temp_arr = np.array(Image.open(i).convert('1')).astype(np.uint8)
                    background+= temp_arr
                    if temp_arr.sum() <= 4:
                        blank_list.append(i)
                        
                except Exception as e:
                    print('Error in mask for ' + str(i) + '\n' + traceback.format_exc() + '\nBackground: ' + str(background.shape) + '\nMask: ' + str(np.array(Image.open(i).convert('1')).astype(np.uint8).shape) + '\nOriginal Mask: ' + str(np.array(Image.open(i)).astype(np.uint8).shape))
                
        if background.sum() <= background.shape[0]*background.shape[1]*args.thr:
            if (args.nonzero and (background.sum() / (background.shape[0]*background.shape[1]) > 0)) or (not args.nonzero):
                if args.rm:
                    for i in file_list:
                        os.remove(i)
                else:
                    out_str = ''
                    for i in range(len(file_list)):
                        if i > 0:
                            out_str = out_str + '\t' + str(file_list[i]) + '\n'
                        elif i == 0:
                            out_str = out_str + str(file_list[i]) + '\tPercent Labeled: ' + '{per:.4%}\n'.format(per=background.sum() / (background.shape[0]*background.shape[1]))
                            #out_str = out_str + str(file_list[i]) + '\tPercent Labeled: ' + '{per:.4%}%\n'.format(per=background.sum() / (background.shape[0]*background.shape[1]))
                    print(out_str)
        elif len(blank_list) > 0:
            for i in blank_list:
                os.remove(i)

    pool = multiprocessing.Pool(multiprocessing.cpu_count()-1) 

    jobs = []

    for curr in filter_for_jpeg(os.path.join(args.directory, 'images'), os.listdir(os.path.join(args.directory, 'images'))):
        p = multiprocessing.Process(target=process_image, args=[os.path.basename(curr)])
        jobs.append(p)
        p.start()

    
    for proc in jobs:
        proc.join()
