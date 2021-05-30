import os
import json
import re
import argparse

import numpy as np
import pandas as pd

from pycocotools.mask import area, decode
import pycocotools.mask as mask_util
from pycococreatortools.pycococreatortools import binary_mask_to_polygon




if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-b","--bbox",dest="bbox",help="Bounding box .json file", default='bbox_coco_val2017_results.json')
    parse.add_argument("-s","--seg",dest="seg",help="Segmentation .json file", default='segmentations_coco_val2017_results.json')
    parse.add_argument("-v","--val",dest="val",help="Validation (or image list) .json file", default='panoptic_val2017_stff.json')
    parse.add_argument("-t","--threshold",dest="threshold",help="Score threshold", default=0.7)
    parse.add_argument("-o","--output",dest="output",help="Output .json file", default='combined_results.json')
    args = parse.parse_args()

    top_dir = "/deac/generalGrp/paucaGrp/dark_mining/UPSNet"
    bbox_file = os.path.join(top_dir,"output/upsnet/mining_resnet101/upsnet_resnet101_mine_2gpu/val2017/results/bbox_coco_val2017_results.json")
    seg_file = os.path.join(top_dir,"output/upsnet/mining_resnet101/upsnet_resnet101_mine_2gpu/val2017/results/segmentations_coco_val2017_results.json")
    val_file = os.path.join(top_dir,"data/coco/annotations/panoptic_val2017_stff.json")

    bbox_file = args.bbox
    seg_file = args.seg
    val_file = args.val

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
        if tem['score'] >= float(args.threshold):
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

    with open(args.output, 'w') as output_json_file:
        json.dump(coco_output, output_json_file)
    