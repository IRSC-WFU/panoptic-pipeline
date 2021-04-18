# panoptic-pipeline: End-to-End Pipeline UPSNet Panoptic Segmentation on a Custom Dataset

# Introduction
This repository exists to take the UPSNet Panoptic Segmentation algorithm and allow a user to build and run it quickly on a new dataset.

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

# Installation
To install this application with UPSNet, please follow these steps
1. Ensure CUDA and GCC versions are loaded and usable.
2. Create the conda environment.
3. Activate the conda environment.
4. Run the `init.sh` script in the top directory.

Assuming all of this can be run without errors (warnings are fine), then UPSNet has been successfully installed.

# Running UPSNet
Depending on what you intend to run with UPSNet, we would refer you to the panoptic-pipeline Github Wiki. We have several options for running.
- Example Datasets
    - We have created two example datasets: shapes and mining. We recommend these datasets for anyone who has not used UPSNet before. Shapes is a dataset for detection of randomly generated shapes. Mining is a dataset used for the detection of dark mining. Both datasets can serve as a gentle introduction to the software and are accompanied by a tutorial.
- UPSNet Datasets
    - UPSNet was initially run on two standard datasets: COCO and Cityscapes. These datasets are much larger than our example datasets and will give the user a feel for what a full run may look like for their datasets. It also serves as a good standard for comparing and benchmarking metrics for custom datasets.
- Custom Datasets
    - The Panoptic Pipeline was designed to allow UPSNet to be generalized to custom datasets. We will include instructions for running on a custom dataset.

For more information on these, see the guides in our Wiki.
