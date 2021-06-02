import datetime
import json
import os
import re
import fnmatch
import argparse

from PIL import Image
import numpy as np
from pycococreatortools import pycococreatortools

INFO = {
    "description": "Dark Mining Dataset",
    "version": "0.1.0",
    "year": 2021,
    "contributor": "Robert Langefeld and Kathering Wang",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

with open('panoptic_coco_categories.json', 'r') as f:
    CATEGORIES = json.load(f)

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
    files = [f for f in files if re.match(
                                    file_name_prefix,
                                    os.path.splitext(os.path.basename(f))[0])
            ]

    return files

if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "-b",
        "--batch",
        dest="batch",
        help="train, test, or val",
        default='train'
    )
    parse.add_argument(
        "-s",
        "--source",
        dest="source",
        help="source directory name",
        default='annotations'
    )
    args = parse.parse_args()

    ROOT_DIR = os.path.join('data', str(args.batch))
    IMAGE_DIR = os.path.join(ROOT_DIR, "images")
    ANNOTATION_DIR = os.path.join(ROOT_DIR, str(args.source))

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    instance_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": [x for x in CATEGORIES if x['isthing'] == 1],
        "images": coco_output['images'],
        "annotations": []
    }

    panoptic_annotations = []

    IMAGE_ID = 1
    SEGMENTATION_ID = 1

    # filter for jpeg images
    for root, _, files in os.walk(IMAGE_DIR):
        image_files = filter_for_jpeg(root, files)

        # go through each image
        for image_filename in image_files:
            print('Adding ' + str(image_filename))
            image = Image.open(image_filename)
            image_info = pycococreatortools.create_image_info(
                IMAGE_ID, os.path.basename(image_filename), image.size)
            coco_output["images"].append(image_info)

            curr_pan_ann = {
                        "IMAGE_ID": IMAGE_ID,
                        "file_name": os.path.basename(os.path.splitext(image_filename)[0]) + '.png',
                        "segments_info": [],
                        }

            # filter for associated png annotations
            for root, _, files in os.walk(ANNOTATION_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:
                    class_id = [x['id']
                                for x in CATEGORIES
                                if x['name'] == annotation_filename.split('_')[1]
                                ][0]
                    print(annotation_filename + '\t' + str(class_id))

                    #category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                    category_info = {
                                    'id': class_id,
                                    'is_crowd': [x['iscrowd']
                                                for x in CATEGORIES
                                                if x['name'] == annotation_filename.split('_')[1]
                                                ][0] == 1
                                    }
                    binary_mask = np.asarray(Image.open(annotation_filename)
                        .convert('1')).astype(np.uint8)

                    annotation_info = pycococreatortools.create_annotation_info(
                        int(os.path.splitext(annotation_filename)[0].split('_')[-1]),
                        IMAGE_ID,
                        category_info,
                        binary_mask,
                        image.size,
                        tolerance=2
                    )

                    if annotation_info is not None:
                        coco_output["annotations"].append(annotation_info)

                        if [x['isthing'] for x in CATEGORIES if x['id'] == class_id][0] == 1:
                            instance_output["annotations"].append(annotation_info)

                        curr_seg_info = {
                                    "id": annotation_info['id'],
                                    "category_id": annotation_info['category_id'],
                                    "area": annotation_info['area'],
                                    "bbox": [int(i) for i in annotation_info['bbox']],
                                    "iscrowd": annotation_info['iscrowd'],
                                }

                        curr_pan_ann['segments_info'].append(curr_seg_info)
                    else:
                        print('\tError with annotation ' + annotation_filename)

                    SEGMENTATION_ID = SEGMENTATION_ID + 1

            panoptic_annotations.append(curr_pan_ann)

            IMAGE_ID = IMAGE_ID + 1

    panoptic_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": coco_output['images'],
        "annotations": panoptic_annotations
    }

    with open(os.path.join(ROOT_DIR, 'coco_' + args.batch + '.json'), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)

    with open(os.path.join(ROOT_DIR, 'panoptic_' + args.batch + '.json'), 'w') as output_json_file:
        json.dump(panoptic_output, output_json_file)

    with open(os.path.join(ROOT_DIR, 'instances_' + args.batch + '.json'), 'w') as output_json_file:
        json.dump(instance_output, output_json_file)
    