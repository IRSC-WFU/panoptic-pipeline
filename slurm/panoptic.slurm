#!/bin/bash
#SBATCH --job-name="panoptic"
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --mem=128GB
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=usb-gpu-04
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=langrc18@wfu.edu
#SBATCH --output=panoptic-%j.o
#SBATCH --error=panoptic-%j.e

cd /deac/generalGrp/paucaGrp/dark_mining/UPSNet

# Load Modules
module load rhel7/gpu/cuda/10.2
module load rhel7/gcc/8.2.0
module load rhel7/gcc/8.2.0-libs

#EXP=upsnet_resnet50_mine_1gpu
EXP=upsnet_resnet101_mine_2gpu
#EXP=upsnet_resnet50_shapes_4gpu

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5

PYTHONPATH=$(pwd)/lib/dataset_devkit:$(pwd)/lib/dataset_devkit/panopticapi:$PYTHONPATH python -u upsnet/upsnet_end2end_train.py --cfg upsnet/experiments/$EXP.yaml
