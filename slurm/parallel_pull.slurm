#!/bin/bash
#SBATCH --job-name="pull-img"
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --mem=64GB
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=pull-img-%j.o
#SBATCH --error=pull-img-%j.e

cd /deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining

python -u parallel_pull.py