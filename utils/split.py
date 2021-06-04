#!/usr/bin/python3
"""This script perform a stratified train-test split for images stored under the ./image folder
while outputing the splitting process and distribution of each class for the train,
val and test dataset"""


import os
import shutil
import json
import argparse

import pandas as pd
from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument(
        "-b",
        "--base",
        dest="base",
        help="Base Directory Name",
        default='images'
    )
    parse.add_argument(
        "-t",
        "--target",
        dest="target",
        help="Target Directory Name",
        default='data'
    )
    parse.add_argument(
        "-c",
        "--categories",
        dest="categories",
        help="Categories JSON File",
        default='panoptic_coco_categories.json'
    )
    parse.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Output csv file",
        default='split_record.csv'
    )
    parse.add_argument(
        "-s",
        "--seed",
        dest="seed",
        help="Random Seed to Use",
        default=42
    )
    args = parse.parse_args()

    BASE_DIR = str(args.base)
    TARGET_DIR = str(args.target)
    seed = int(args.seed)

    with open(args.categories, 'r') as f:
        CATEGORIES = json.load(f)

    cat_list = [x['name'] for x in CATEGORIES]

    data_dict = {
                    'train' : [0]*len(cat_list),
                    'val' : [0]*len(cat_list),
                    'test' : [0]*len(cat_list)
                }

    images = {}

    train_images = []
    test_images = []
    val_images = []

    train_ann = []
    test_ann = []
    val_ann = []

    # Directory Setup
    print('Making directories')
    for curr_split in ['train', 'val', 'test']:
        print('\tMaking ' + curr_split + ' split')
        if not os.path.exists(os.path.join(TARGET_DIR, curr_split,'images')):
            os.makedirs(os.path.join(TARGET_DIR, curr_split,'images'))
        if not os.path.exists(os.path.join(TARGET_DIR, curr_split,'annotations')):
            os.makedirs(os.path.join(TARGET_DIR, curr_split,'annotations'))

    train_images, val_images = train_test_split(
                                    os.listdir(os.path.join(BASE_DIR, 'images')),
                                    test_size=0.40,
                                    shuffle=True,
                                    random_state=seed
                                )
    val_images, test_images = train_test_split(
                                    val_images,
                                    test_size=0.20,
                                    shuffle=True,
                                    random_state=seed
                                )

    train_names = [os.path.splitext(i)[0] for i in train_images]
    test_names = [os.path.splitext(i)[0] for i in test_images]
    val_names = [os.path.splitext(i)[0] for i in val_images]

    for img in train_names:
        for i in os.listdir(os.path.join(BASE_DIR, 'annotations')):
            if img in i:
                train_ann.append(i)

    for img in test_names:
        for i in os.listdir(os.path.join(BASE_DIR, 'annotations')):
            if img in i:
                test_ann.append(i)

    for img in val_names:
        for i in os.listdir(os.path.join(BASE_DIR, 'annotations')):
            if img in i:
                val_ann.append(i)

    # Move
    print('Moving Images')

    IMAGE_SET = zip(
                    ['train', 'val', 'test'],
                    [train_images, val_images, test_images],
                    [train_ann, val_ann, test_ann]
                )

    for curr_split, curr_images, curr_ann in IMAGE_SET:
        print('\tMoving ' + curr_split + ' images')
        dest_dir = TARGET_DIR + '/' + curr_split

        for img in curr_images:
            image_dir = os.path.join(BASE_DIR, 'images')

            shutil.copyfile(
                os.path.join(image_dir,img),
                os.path.join(dest_dir,'images', os.path.basename(img))
            )

        for img in curr_ann:
            anno_dir = os.path.join(BASE_DIR, 'annotations')
            if os.path.basename(img).split('_')[1] in cat_list:
                shutil.copyfile(
                    os.path.join(anno_dir,img),
                    os.path.join(dest_dir, 'annotations', os.path.basename(img))
                )
                IDX = cat_list.index(os.path.basename(img).split('_')[1])
                data_dict[curr_split][IDX]+= 1

    split_data = {
                'Name'  : train_images + val_images + test_images,
                'Split' : ['train']*len(train_images) +
                        ['validation']*len(val_images) +
                        ['test']*len(test_images)
                }

    record_data = pd.DataFrame.from_dict(split_data)
    record_data.to_csv(str(args.output), index=False)

    cat_df = pd.DataFrame(data_dict, index=cat_list)
    print(cat_df)
