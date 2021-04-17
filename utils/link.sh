#!/bin/bash

# Declare Variables
TOP=$(pwd)
BASE=$TOP
COCO=$TOP/UPSNet/data/coco

# Convert Coco Files
python coco_convert.py -b train
python coco_convert.py -b val
python coco_convert.py -b test

# Convert to Panoptic Files
python pixelMap.py -b train
python pixelMap.py -b val
python pixelMap.py -b test

# Make Directories
mkdir -p $COCO
mkdir -p $COCO/annotations
mkdir -p $COCO/images

################
# Unlink Files #
################

# Unlink Annotation Files
rm $COCO/annotations/coco_train.json
rm $COCO/annotations/coco_val.json
rm $COCO/annotations/coco_test.json

# Unlink Panoptic Files
rm $COCO/annotations/panoptic_train2017.json
rm $COCO/annotations/panoptic_val2017.json
rm $COCO/annotations/panoptic_test2017.json

# Unlink Instance Files
rm $COCO/annotations/instances_train2017.json
rm $COCO/annotations/instances_val2017.json
rm $COCO/annotations/instances_test2017.json

# Unlink Image Directories
rm $COCO/images/train2017
rm $COCO/images/val2017
rm $COCO/images/test2017

# Unlink Panoptic Directories
rm $COCO/annotations/panoptic_train2017
rm $COCO/annotations/panoptic_val2017
rm $COCO/annotations/panoptic_test2017

# Unlink Categories File
rm $COCO/annotations/panoptic_coco_categories.json

##############
# Link Files #
##############

# Link Annotation Files
# ln -s $BASE/coco_train.json $COCO/annotations/coco_train.json
# ln -s $BASE/coco_val.json $COCO/annotations/coco_val.json
# ln -s $BASE/coco_test.json $COCO/annotations/coco_test.json

mv $BASE/coco_train.json $COCO/annotations/coco_train.json
mv $BASE/coco_val.json $COCO/annotations/coco_val.json
mv $BASE/coco_test.json $COCO/annotations/coco_test.json

# Link Panoptic Files
# ln -s $BASE/panoptic_train.json $COCO/annotations/panoptic_train2017.json
# ln -s $BASE/panoptic_val.json $COCO/annotations/panoptic_val2017.json
# ln -s $BASE/panoptic_test.json $COCO/annotations/panoptic_test2017.json

mv $BASE/panoptic_train.json $COCO/annotations/panoptic_train2017.json
mv $BASE/panoptic_val.json $COCO/annotations/panoptic_val2017.json
mv $BASE/panoptic_test.json $COCO/annotations/panoptic_test2017.json

# Link Instance Files
# ln -s $BASE/instances_train.json $COCO/annotations/instances_train2017.json
# ln -s $BASE/instances_val.json $COCO/annotations/instances_val2017.json
# ln -s $BASE/instances_test.json $COCO/annotations/instances_test2017.json

mv $BASE/instances_train.json $COCO/annotations/instances_train2017.json
mv $BASE/instances_val.json $COCO/annotations/instances_val2017.json
mv $BASE/instances_test.json $COCO/annotations/instances_test2017.json

# Link Image Directories
ln -s $BASE/data/train/images $COCO/images/train2017
ln -s $BASE/data/val/images $COCO/images/val2017
ln -s $BASE/data/test/images $COCO/images/test2017

# Link Panoptic Directories
ln -s $BASE/data/train/pixelMap $COCO/annotations/panoptic_train2017
ln -s $BASE/data/val/pixelMap $COCO/annotations/panoptic_val2017
ln -s $BASE/data/test/pixelMap $COCO/annotations/panoptic_test2017

# Link Categories File
cp $BASE/panoptic_coco_categories.json $COCO/annotations/panoptic_coco_categories.json
