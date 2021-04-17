import json
import requests
import os
import argparse
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import cv2
import matplotlib.pyplot as plt

def index_to_class(index):
    index = int(index)
    order = ['other',
            'float',
            'heavy-machinery',
            'hose',
            'dredge',
            'sluice',
            'tailing-dark-mine',
            'tailing',
            'roof-top',
            'shack',
            'road',
            'residual-pond',
            'river',
            'sand-river-bank',
            'deforested-area']
    return order[index]
    


if __name__ == '__main__':

    parse = argparse.ArgumentParser()
    parse.add_argument("-b","--batch",dest="batch",help="train, test, or val",default='train')
    args = parse.parse_args()

    imgfolder = '/deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining/data/' + str(args.batch) + '/categorical_masks'
    path_target = '/deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining/data/' + str(args.batch) + '/nonoverlapping_annotations1'
    if not os.path.exists(path_target):
        os.makedirs(path_target)
    
    
    for backgroundfile in os.listdir(imgfolder):
        backgroundfile1 = backgroundfile.split('.')
        img = np.array(Image.open(os.path.join(imgfolder,backgroundfile)), dtype=np.uint8)
        print('Generating non-overlapping annotation for: ' + str(os.path.join(imgfolder,backgroundfile)))
        instance_id = np.unique(img.reshape(-1, img.shape[2]), axis=0)
        #instance_id = np.unique(img[:,:,1])
        height, width, _ = np.array(img).shape

        for i in instance_id:
            curr_class = index_to_class(i[0])
            curr_id = i[1]
            newImg = np.zeros([height,width,3],dtype=np.uint8)
            newImg[np.all(img == i, axis=-1)] = [255,255,255]

            
            mask_name = os.path.join(path_target,str(os.path.splitext(os.path.basename(backgroundfile))[0]).replace('_', '-') + '_' + str(curr_class) + '_' + str(curr_id) + '.png')
            newImg = Image.fromarray(newImg)
            newImg.save(mask_name,cmap=plt.get_cmap('gray'))
