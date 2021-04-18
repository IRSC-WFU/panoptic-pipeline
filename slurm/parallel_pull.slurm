#!/bin/bash
#SBATCH --job-name="pull-img"
#SBATCH --partition=small
#SBATCH --nodes=1
#SBATCH --tasks-per-node=16
#SBATCH --mem=64GB
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=slurm/pull-img-%j.o
#SBATCH --error=slurm/pull-img-%j.e

python -u utils/parallel_pull.py