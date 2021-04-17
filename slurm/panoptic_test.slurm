#!/bin/bash
#SBATCH --job-name="panoptic-test"
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --mem=128GB
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=usb-gpu-01
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=panoptic-test-%j.o
#SBATCH --error=panoptic-test-%j.e

cd /deac/generalGrp/paucaGrp/dark_mining/UPSNet

# Load Modules
module load rhel7/gpu/cuda/10.2
module load rhel7/gcc/8.2.0
module load rhel7/gcc/8.2.0-libs

#EXP=upsnet_resnet50_mine_1gpu
EXP=upsnet_resnet101_mine_2gpu
#EXP=upsnet_resnet50_shapes_4gpu

#export CUDA_VISIBLE_DEVICES=0,1,2,3
#export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5
export CUDA_VISIBLE_DEVICES=0,1

PYTHONPATH=$(pwd)/lib/dataset_devkit:$(pwd)/lib/dataset_devkit/panopticapi:$PYTHONPATH python -u upsnet/upsnet_end2end_test.py --cfg upsnet/experiments/$EXP.yaml