#!/bin/sh
. /local/env/envconda.sh

WD=$(pwd)
export CONDA_ALWAYS_YES="true"

# init env
conda create -p $WD"/.env" python=3.11

# activate env to install packages
conda activate $WD"/.env"

# installing vgtools, minimap2, minigraph
conda install -c bioconda minimap2
conda install -c bioconda minigraph
conda install -c bioconda vg
conda install -c bioconda odgi

# installing packages
python -m pip install -r requirements.txt

unset CONDA_ALWAYS_YES
conda deactivate
