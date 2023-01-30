#!/bin/sh
. /local/env/envconda.sh


WD=$(pwd)
export CONDA_ALWAYS_YES="true"

# init env
conda create -p $WD"/.env_bdsg" python=3.7

# activate env to install packages
conda activate $WD"/.env_bdsg"

# requirements for bdsg
conda install -c conda-forge doxygen


python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install --upgrade wheel
# installing required python packages
python -m pip install -r requirements.txt

unset CONDA_ALWAYS_YES
conda deactivate
