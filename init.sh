#!/bin/bash

# Declare Variables
TOP=$(pwd)

#######################
#  Initialize UPSNet  #
#######################

git clone git@github.com:uber-research/UPSNet.git

cd $TOP/UPSNet

bash init.sh

cd $TOP

#########################
#  Copy Modified Files  #
#########################

cp $TOP/utils/upsnet-custom/base_dataset.py $TOP/UPSNet/upsnet/dataset/base_dataset.py

cp $TOP/utils/upsnet-custom/init_dataset.sh $TOP/UPSNet/init_dataset.sh

cp $TOP/utils/upsnet-custom/init_dataset.py $TOP/UPSNet/init_dataset.py

cp $TOP/utils/upsnet-custom/upsnet_end2end_test.py $TOP/UPSNet/upsnet/upsnet_end2end_test.py

mkdir logs
