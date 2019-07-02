#!/bin/bash


# Installing Anaconda
if which conda; then
	echo "Anaconda already installed."
else
	wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
	bash Anaconda3-2019.03-Linux-x86_64.sh
	rm -f Anaconda3-2019.03-Linux-x86_64.sh
	conda init bash
	echo "Please open a new terminal and rerun this script (using source command, not bash) to continue setup."
	exit 0
fi


# Setting up virtual environment
echo "Please enter a name for the conda virtual environment:"
read env_name
conda create -n $env_name numpy=1.16.0 tensorflow-gpu=1.12 cudatoolkit=9.0 tqdm scikit-image keras cython
conda activate $env_name
pip install autolab_core request --ignore-installed


# Clone sd-maskrcnn git repository
git clone https://github.com/Sean-Hastings/sd-maskrcnn.git
cd sd-maskrcnn
bash install.sh generation
pip install -e . --ignore-installed
pip install -e ./maskrcnn --ignore-installed


# Install Wisdom dataset
echo "Would you like to install the Wisdom-Real dataset? (y/n)"
read response
if [[ $response =~ ^[Yy]$ ]]; then
mkdir datasets
cd datasets
mkdir wisdom
cd wisdom
wget https://berkeley.box.com/shared/static/7aurloy043f1py5nukxo9vop3yn7d7l3.rar
file-roller 7aurloy043f1py5nukxo9vop3yn7d7l3.rar --extract-to .
rm -f 7aurloy043f1py5nukxo9vop3yn7d7l3.rar
cd ../..
fi


# Install plane urdf
mkdir datasets
cd datasets
mkdir objects
cd objects
mkdir urdf
cd urdf
mkdir cache
cd cache
mkdir plane
cd plane
wget https://raw.githubusercontent.com/BerkeleyAutomation/sd-maskrcnn/497264f934aad75fd3d795f138523fdcc151b223/sd_maskrcnn/data/plane/plane_convex_piece_0.obj
wget https://raw.githubusercontent.com/BerkeleyAutomation/sd-maskrcnn/497264f934aad75fd3d795f138523fdcc151b223/sd_maskrcnn/data/plane/plane_pose.tf
wget https://raw.githubusercontent.com/BerkeleyAutomation/sd-maskrcnn/497264f934aad75fd3d795f138523fdcc151b223/sd_maskrcnn/data/plane/plane.obj
wget https://raw.githubusercontent.com/BerkeleyAutomation/sd-maskrcnn/497264f934aad75fd3d795f138523fdcc151b223/sd_maskrcnn/data/plane/plane.urdf
cd ../../../../..


# Redo some package installations because this seems to be necessary
yes | pip uninstall tensorflow tensorflow-gpu keras keras scikit-image cudatoolkit cudnn
yes | conda uninstall tensorflow tensorflow-gpu keras keras scikit-image cudatoolkit cudnn
yes | conda install tensorflow tensorflow-gpu keras scikit-image keras cudatoolkit=9.0 cudnn
yes | pip uninstall keras
yes | pip install keras


sed -i -e 's/use_multiprocessing=True/use_multiprocessing=False/g' maskrcnn/mrcnn/model.py
