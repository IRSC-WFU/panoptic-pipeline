import os
import re
import argparse

import numpy as np
from scipy.stats import iqr

import multiprocessing

from PIL import Image
import cv2

def contour_image(image_name):
    print('Processing:', image_name)
    # Open image
    img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

    # Threshold object sizes
    # Adapted from https://stackoverflow.com/questions/42798659/how-to-remove-small-connected-objects-using-opencv
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=4)
    sizes = stats[1:, -1]; nb_components = nb_components - 1
    
    iqr_size = iqr(sizes)
    mean_size = np.mean(sizes)
    min_size = mean_size - (iqr_size*5)

    img2 = np.zeros((output.shape), dtype='uint8')
    #for every component in the image, you keep it only if it's above min_size
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = img[output == i + 1]

    img = img2


    # Pull contours
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    object_count = 0

    img = img.astype('bool')

    c = cnts[0]
    for i in range(len(cnts[0])):
        background = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        cv2.drawContours(background, c, i, 255, thickness=cv2.FILLED)

        background = background.astype('bool') & img

        object_path = str(os.path.splitext(image_name)[0]) + '_' + str(object_count) + str(os.path.splitext(image_name)[1])
        Image.fromarray(background).save(object_path)
        #cv2.imwrite(object_path, background)
        object_count+=1
    
    os.remove(image_name)

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-d","--directory",dest="directory",help="Directory to run splitting on",default='images/annotations')
    args = parse.parse_args()

    for root, _, files in os.walk(args.directory):
        png_files = [i for i in files if ".png" in i]

        pool = multiprocessing.Pool(multiprocessing.cpu_count()-1) 

        jobs = []

        for name in png_files:
            p = multiprocessing.Process(target=contour_image, args=(os.path.join(root,name),))
            jobs.append(p)
            p.start()

        for p in jobs:
            p.join()

for root, _, files in os.walk('images/annotations'):
    png_files = [i for i in files if ".png" in i]

    object_count = 0

    for name in png_files:
        new_name = '_'.join(name.split('_')[:-2]) + '_' + str(object_count) + os.path.splitext(name)[1]
        os.rename(os.path.join(root,name), os.path.join(root,new_name))
        object_count+=1
        


