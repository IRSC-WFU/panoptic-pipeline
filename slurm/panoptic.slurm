#!/bin/bash
#SBATCH --job-name="panoptic"
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --mem=128GB
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=usb-gpu-01
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=logs/panoptic-%j.o
#SBATCH --error=logs/panoptic-%j.e

TOP=$(pwd)

cd UPSNet

# Load Modules
module load rhel7/gpu/cuda/10.2
module load rhel7/gcc/8.2.0
module load rhel7/gcc/8.2.0-libs

EXP=upsnet_resnet101_mine_2gpu

export CUDA_VISIBLE_DEVICES=0,1

PYTHONPATH=$(pwd)/lib/dataset_devkit:$(pwd)/lib/dataset_devkit/panopticapi:$PYTHONPATH python -u upsnet/upsnet_end2end_train.py --cfg $TOP/experiments/$EXP.yaml
