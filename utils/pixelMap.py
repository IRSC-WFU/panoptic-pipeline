import numpy as np
import cv2
import os
import argparse
from PIL import Image
import json

def label_to_color(input_string):
    x = int(input_string)

    R = x % 256
    x//=256
    G = x % 256
    x//=256
    B = x % 256
    return [R, G, B]


def rgb2id(color):
    if isinstance(color, np.ndarray) and len(color.shape) == 3:
        if color.dtype == np.uint8:
            color = color.astype(np.int32)
        return color[:, :, 0] + 256 * color[:, :, 1] + 256 * 256 * color[:, :, 2]
    return int(color[0] + 256 * color[1] + 256 * 256 * color[2])

def processMask(mask,color):
    mask[np.where((mask == [255,255,255] ).all(axis = 2))] = color
    return mask

def id2rgb(id_map):
    if isinstance(id_map, np.ndarray):
        id_map_copy = id_map.copy()
        rgb_shape = tuple(list(id_map.shape) + [3])
        rgb_map = np.zeros(rgb_shape, dtype=np.uint8)
        for i in range(3):
            rgb_map[..., i] = id_map_copy % 256
            id_map_copy //= 256
        return rgb_map
    color = []
    for _ in range(3):
        color.append(id_map % 256)
        id_map //= 256
    return color

if __name__ == '__main__':
    instanceId = 0
    ID_dict = {}
    parse = argparse.ArgumentParser()
    parse.add_argument("-b","--batch",dest="batch",help="train, test, or val",default='train')
    parse.add_argument("-s","--source",dest="source",help="Source Directory Name",default='annotations')
    parse.add_argument("-o","--output",dest="output",help="Output Directory",default=os.path.join(os.getcwd(), 'data'))
    args = parse.parse_args()

    # folder = '/deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining/data/' + str(args.batch) + '/' + str(args.source)
    # imgfolder = '/deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining/data/' + str(args.batch) + '/images'
    folder = os.path.join(str(args.output), str(args.batch), str(args.source))
    imgfolder = os.path.join(str(args.output), str(args.batch), 'images')

    for backgroundfile in os.listdir(imgfolder):
        print('Masking ' + str(backgroundfile))
        backgroundfile1 = backgroundfile.split('.')
        background = cv2.imread(os.path.join(imgfolder,backgroundfile))
        height= background.shape[0]
        width= background.shape[1]
        background = np.zeros([height,width,3],dtype=np.uint8)
        background.fill(0)
        
        masks = []
        id_list = []
        for filename in os.listdir(folder):
            filename1 = filename.split('_')
            filetem = filename.split('.')
            if filename1[0] == backgroundfile1[0]:
                img = cv2.imread(os.path.join(folder,filename))
                #img = np.array(Image.open(os.path.join(folder,filename)))
                #img = processMask(img,label_to_color(filename1[1]))
                #color = label_to_color(os.path.splitext(filename)[0].split('_')[-1])
                color = id2rgb(int(os.path.splitext(filename)[0].split('_')[-1]))
                #id_list.append(int(os.path.splitext(filename)[0].split('_')[-1]))
                id_list.append(filename)
                assert rgb2id(color) == int(os.path.splitext(filename)[0].split('_')[-1])
                
                img = processMask(img,color)
                
                masks.append(img)
            
        i=0
        for mask in masks:
            assert ((background != 0) & (mask != 0)).sum() == 0
            background = background + mask # equivalent to background[mask != 0] = mask[mask != 0]
            i+=1
            

        # path = '/deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining/data/' + str(args.batch) + '/pixelMap'
        path = os.path.join(str(args.output), str(args.batch), 'pixelMap')
        if not os.path.exists(path):
            os.makedirs(path)
        #cv2.imwrite(os.path.join(path,'{0}.png'.format(backgroundfile1[0])), background)
        Image.fromarray(background).save(os.path.join(path,'{0}.png'.format(backgroundfile1[0])))
        

