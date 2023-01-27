ENV=".env/"

if [ -d "$ENV" ];
then
    rm -r $ENV
else
	echo "Creating env..."
fi

WD=$(pwd)
export CONDA_ALWAYS_YES="true"

# init env
conda create -p $WD"/.env" python=3.7

# activate env to install packages
conda activate $WD"/.env"

# installing required python packages
python -m pip install --upgrade pip
pip install wheel
pip install --upgrade setuptools wheel
pip install -r requirements.txt --no-cache-dir

unset CONDA_ALWAYS_YES
conda deactivate