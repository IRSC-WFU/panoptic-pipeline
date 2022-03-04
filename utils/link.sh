#!/bin/bash

# Declare Variables
TOP=$(pwd)
BASE=$TOP
COCO=$TOP/UPSNet/data/coco

# Modify filenames to work with Python re
# Note this replaces characters that could interfere with regexes
echo "Converting Image Names to Valid Characters"
python $TOP/utils/name_convert.py -g train
python $TOP/utils/name_convert.py -g val
python $TOP/utils/name_convert.py -g test

# Convert Coco Files
echo "Converting Image Annotations to Coco Format and Generate JSON Files"
python $TOP/utils/coco_convert.py -b train
python $TOP/utils/coco_convert.py -b val
python $TOP/utils/coco_convert.py -b test

# Convert to Panoptic Files
echo "Constructing Pixel Map for Images"
python $TOP/utils/pixelMap.py -b train
python $TOP/utils/pixelMap.py -b val
python $TOP/utils/pixelMap.py -b test

# Make Directories
echo "Making Directories"
mkdir -p $COCO
mkdir -p $COCO/annotations
mkdir -p $COCO/images

################
# Unlink Files #
################

echo "Unlinking Old Files (If They Exist)"

# Unlink Annotation Files
rm $COCO/annotations/coco_train.json 2>/dev/null
rm $COCO/annotations/coco_val.json 2>/dev/null
rm $COCO/annotations/coco_test.json 2>/dev/null

# Unlink Panoptic Files
rm $COCO/annotations/panoptic_train2017.json 2>/dev/null
rm $COCO/annotations/panoptic_val2017.json 2>/dev/null
rm $COCO/annotations/panoptic_test2017.json 2>/dev/null

# Unlink Instance Files
rm $COCO/annotations/instances_train2017.json 2>/dev/null
rm $COCO/annotations/instances_val2017.json 2>/dev/null
rm $COCO/annotations/instances_test2017.json 2>/dev/null

# Unlink Image Directories
rm $COCO/images/train2017 2>/dev/null
rm $COCO/images/val2017 2>/dev/null
rm $COCO/images/test2017 2>/dev/null

# Unlink Panoptic Directories
rm $COCO/annotations/panoptic_train2017 2>/dev/null
rm $COCO/annotations/panoptic_val2017 2>/dev/null
rm $COCO/annotations/panoptic_test2017 2>/dev/null

# Unlink Categories File
rm $COCO/annotations/panoptic_coco_categories.json 2>/dev/null

##############
# Link Files #
##############

echo "Linking New Files"

# Link Annotation Files
# ln -s $BASE/coco_train.json $COCO/annotations/coco_train.json
# ln -s $BASE/coco_val.json $COCO/annotations/coco_val.json
# ln -s $BASE/coco_test.json $COCO/annotations/coco_test.json

echo "Moving Annotation JSON Files"
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

echo "Linking Image and Annotation Directories"
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
