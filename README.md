# Panoptic Pipeline: End-to-End Pipeline for UPSNet Panoptic Segmentation on a Custom Dataset

# Introduction
This repository exists to take the UPSNet Panoptic Segmentation algorithm and allow a user to build and run it quickly on a new dataset. It was made as an extension of the [UPSNet](https://github.com/uber-research/UPSNet) repository.

# License

# Citing panoptic-pipeline

# Requirements: Software
Compiling and running UPSNet has several software requirements.
It may run with other software configurations, but this is what we have tested with:
- CUDA 10.2
- GCC 8.2.0
- Python 3.6
    - PyTorch 0.4.1
    - pycococreatortools 0.2.0
    - pycocotools 2.0.2

Our Python environment was created using Miniconda. We recommend this as the easiest way to duplicate this environment.

# Requirements: Hardware
This software requires an Nvidia GPU. We have currently tested with on Nvidia P100 and V100 GPUs.
For the most efficient code, we recommend running with multiple GPUs to speed up training.
Additionally, this code scales well with an increase in processor number.

# Installation <a name="installation"></a>
To install this application with UPSNet, please follow these steps
1. Ensure CUDA and GCC versions are loaded and usable.
2. Create the conda environment.
3. Activate the conda environment.
4. Run the `init.sh` script in the top directory.

Assuming all of this can be run without errors (warnings are fine), then UPSNet has been successfully installed.

# Running UPSNet
Depending on what you intend to run with UPSNet, we would refer you to the docs section. We have several options for running.
- Example Datasets
    - We have created two example datasets: shapes and mining. We recommend these datasets for anyone who has not used UPSNet before. [Shapes](#shapes) is a dataset for detection of randomly generated shapes. [Mining](#mining) is a dataset used for the detection of dark mining. Both datasets can serve as a gentle introduction to the software and are accompanied by a tutorial.
- UPSNet Datasets
    - UPSNet was initially run on two standard datasets: COCO and Cityscapes. These datasets are much larger than our example datasets and will give the user a feel for what a full run may look like for their datasets. It also serves as a good standard for comparing and benchmarking metrics for custom datasets.
- Custom Datasets
    - The Panoptic Pipeline was designed to allow UPSNet to be generalized to custom datasets. We will include instructions for running on a custom dataset.

For more information on these, see the guides in the docs.

# Example: Shapes <a name="shapes"></a>
Make sure UPSNet is installed and initialized as described in [installation](#installation). All scripts should be run from the `panoptic-pipeline` directory.

1. To create the shapes dataset, begin by running the `basic_generate.py` script, located in `panoptic-pipeline/examples/shapes`.
2. Run `cp examples/shapes/panoptic_coco_categories.json .` to copy the `panoptic_coco_categories.json` file to the top directory.
3. Run `utils/split.py` to create a train-val-test split on the dataset.
4. Run `bash utils/link.sh` to generate important JSON files, move them, and symlink the generated data.
5. Run `bash UPSNET/init_dataset.sh`.
6. Run `bash slurm/panoptic.slurm` to train the model. Please be sure to modify `CUDA_VISIBLE_DEVICES` and the shapes config file in `panoptic-pipelines/experiments` to reflect your system.
7. Run `bash slurm/panoptic_test.slurm` to train the model. Please be sure to modify `CUDA_VISIBLE_DEVICES` and the shapes config file in `panoptic-pipelines/experiments` to reflect your system.

# Example: Mining <a name="mining"></a>
Make sure UPSNet is installed and initialized as described in [installation](#installation). All scripts should be run from the `panoptic-pipeline` directory.

1. Run `cp examples/mining/info.json .` to copy the `info.json` file to the top directory.
2. Run `python parallel_pull.py` to pull all required files from LabelBox.
3. Run `cp examples/mining/panoptic_coco_categories.json .` to copy the `panoptic_coco_categories.json` file to the top directory.
4. Run `utils/split.py` to create a train-val-test split on the dataset.
5. Run `bash utils/link.sh` to generate important JSON files, move them, and symlink the generated data.
6. Run `bash UPSNET/init_dataset.sh`.
7. Run `bash slurm/panoptic.slurm` to train the model. Please be sure to modify `CUDA_VISIBLE_DEVICES` and the shapes config file in `panoptic-pipelines/experiments` to reflect your system.
8. Run `bash slurm/panoptic_test.slurm` to train the model. Please be sure to modify `CUDA_VISIBLE_DEVICES` and the shapes config file in `panoptic-pipelines/experiments` to reflect your system.

# Examples: COCO and Cityscapes
Please see the [UPSNet](https://github.com/uber-research/UPSNet) repository and documentation for how to test on COCO and Cityscapes data. Note that this is much more challenging and is not recommended for beginners or those without Linux experience.

# Custom Dataset <a name="custom"></a>
Make sure UPSNet is installed and initialized as described in [installation](#installation). All scripts should be run from the `panoptic-pipeline` directory. Additionally, note that UPSNet (and panoptic segmentation in general) requires that binary masks provided are non-overlapping. If this is not the case, we cannot guarantee that the scripts will run and cannot trust the validity of the results.

1. If annotations are stored in the "segmentations" format in LabelBox, the generate your segmentation output file and store it in the top directory as `info.json`. If annotations are already in a binary mask format, please copy the images to `panoptic-pipeline/images` and the masks to `panoptic-pipeline/annotations` and skip to step 3.
2. Run `python parallel_pull.py` to pull all required files from LabelBox.
3. Use either `examples/mining/panoptic_coco_categories.json` or `examples/shapes/panoptic_coco_categories.json` to create your own `panoptic_coco_categories.json` file in the top directory. Please notice the difference between "things" and "stuff" classes (documented in [COCO](https://cocodataset.org/)).
4. Run `utils/split.py` to create a train-val-test split on the dataset.
5. Run `bash utils/link.sh` to generate important JSON files, move them, and symlink the generated data.
6. Run `bash UPSNET/init_dataset.sh`.
7. Run `bash slurm/panoptic.slurm` to train the model. Please be sure to modify `CUDA_VISIBLE_DEVICES` and the shapes config file in `panoptic-pipelines/experiments` to reflect your system.
8. Run `bash slurm/panoptic_test.slurm` to train the model. Please be sure to modify `CUDA_VISIBLE_DEVICES` and the shapes config file in `panoptic-pipelines/experiments` to reflect your system.

# Authors
- [@rlangefe](https://github.com/rlangefe) - 
- [@LexieKatherine](https://github.com/LexieKatherine) - 