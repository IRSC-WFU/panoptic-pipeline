import os
import json
import re

import numpy as np
import pandas as pd

from pycocotools.mask import area, decode
import pycocotools.mask as mask_util
from pycococreatortools.pycococreatortools import binary_mask_to_polygon




if __name__ == '__main__':
    top_dir = "/deac/generalGrp/paucaGrp/dark_mining/UPSNet"
    bbox_file = os.path.join(top_dir,"output/upsnet/mining_resnet101/upsnet_resnet101_mine_2gpu/val2017/results/bbox_coco_val2017_results.json")
    seg_file = os.path.join(top_dir,"output/upsnet/mining_resnet101/upsnet_resnet101_mine_2gpu/val2017/results/segmentations_coco_val2017_results.json")
    catfile = os.path.join(top_dir,"data/coco/annotations/panoptic_coco_categories_stff.json")
    val_file = os.path.join(top_dir,"data/coco/annotations/panoptic_val2017_stff.json")


    with open(catfile, 'r') as f:
        CATEGORIES = json.load(f)

    with open(bbox_file, 'r') as f:
        bbox = json.load(f)

    with open(seg_file, 'r') as f:
        seg = json.load(f)

    with open(val_file, 'r') as f:
        val = json.load(f)
    
    INFO = val['info']
    LICENSES = val['licenses']
    CATEGORIES = val['categories']

    annot = []
    count = 1
    for i in range(0, len(seg)):
        tem = bbox[i]
        tem['id'] = count
        tem['iscrowd'] = CATEGORIES[bbox[i]['category_id']]['iscrowd']
        tem['area'] = float(area(seg[i]['segmentation']))
        #tem['segmentation'] = seg[i]['segmentation']

        if tem['iscrowd'] == 0:
            tem['segmentation'] = binary_mask_to_polygon(decode(seg[i]['segmentation']), tolerance=0)
        else:
            tem['segmentation'] = seg[i]['segmentation']

        annot.append(tem)
        count += 1
        
    IMAGES = []

    for i in val['images']:
        i['file_name'] = os.path.splitext(i['file_name'])[0] + '.jpg'
        IMAGES.append(i)

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": IMAGES,
        "annotations": annot
    }

    with open('labels.json', 'w') as output_json_file:
        json.dump(coco_output, output_json_file)
        
    
    
    
    