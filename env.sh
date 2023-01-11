#!/bin/sh
. /local/env/envconda.sh


WD=$(pwd)
export CONDA_ALWAYS_YES="true"

# init env
conda create -p $WD"/.env" python=3.10

# activate env to install packages
conda activate $WD"/.env"

# installing vgtools, minimap2, minigraph
conda install -c bioconda minimap2
conda install -c bioconda minigraph
conda install -c bioconda vg
conda install -c bioconda odgi

# get deps minigraph-cactus : bzip2
. /local/env/envhtslib-1.6.sh

# installing required python packages
python -m pip install -r requirements.txt

# getting cactus from source
git clone https://github.com/ComparativeGenomicsToolkit/cactus.git --recursive
cd cactus
python -m pip install -U setuptools pip
python -m pip install -U -r ./toil-requirement.txt
python -m pip install -U .
grep apt-get Dockerfile | head -1 | sed -e 's/RUN //g' -e 's/apt-get/sudo apt-get/g'
make -j 8
build-tools/downloadPangenomeTools

unset CONDA_ALWAYS_YES
conda deactivate
