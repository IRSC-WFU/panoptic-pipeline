# PYTHONPATH=$(pwd)/lib/dataset_devkit:$(pwd)/lib/dataset_devkit/panopticapi:$PYTHONPATH python lib/dataset_devkit/panopticapi/converters/detection2panoptic_coco_format.py \
#   --input_json_file data/coco/annotations/coco_train.json \
#   --output_json_file data/coco/annotations/panoptic_train2017.json \
#   --categories_json_file data/coco/annotations/panoptic_coco_categories.json \
#   --segmentations_folder data/coco/annotations/panoptic_train2017

# PYTHONPATH=$(pwd)/lib/dataset_devkit:$(pwd)/lib/dataset_devkit/panopticapi:$PYTHONPATH python lib/dataset_devkit/panopticapi/converters/detection2panoptic_coco_format.py \
#   --input_json_file data/coco/annotations/coco_val.json \
#   --output_json_file data/coco/annotations/panoptic_val2017.json \
#   --categories_json_file data/coco/annotations/panoptic_coco_categories.json \
#   --segmentations_folder data/coco/annotations/panoptic_val2017

##################################
# Run Initializing Python Script #
##################################

python init_mining.py


#cp data/coco/annotations/coco_train.json data/coco/annotations/instances_train2017.json
#cp data/coco/annotations/coco_val.json data/coco/annotations/instances_val2017.json

###############################
# Pull Semantic from Panoptic #
###############################

sed -i 's/semantic = np.zeros(pan.shape, dtype=np.uint8)/semantic = np.ones(pan.shape, dtype=np.uint8) * 255/g' lib/dataset_devkit/panopticapi/converters/panoptic2semantic_segmentation.py

PYTHONPATH=$(pwd)/lib/dataset_devkit:$(pwd)/lib/dataset_devkit/panopticapi:$PYTHONPATH python lib/dataset_devkit/panopticapi/converters/panoptic2semantic_segmentation.py \
  --input_json_file data/coco/annotations/panoptic_train2017_stff.json \
  --segmentations_folder data/coco/annotations/panoptic_train2017 \
  --semantic_seg_folder data/coco/annotations/panoptic_train2017_semantic_trainid_stff \
  --categories_json_file data/coco/annotations/panoptic_coco_categories_stff.json

PYTHONPATH=$(pwd)/lib/dataset_devkit:$(pwd)/lib/dataset_devkit/panopticapi:$PYTHONPATH python lib/dataset_devkit/panopticapi/converters/panoptic2semantic_segmentation.py \
  --input_json_file data/coco/annotations/panoptic_val2017_stff.json \
  --segmentations_folder data/coco/annotations/panoptic_val2017 \
  --semantic_seg_folder data/coco/annotations/panoptic_val2017_semantic_trainid_stff \
  --categories_json_file data/coco/annotations/panoptic_coco_categories_stff.json 
