REL_TAG=v2.4.0
tar -xzf "cactus-bin-${REL_TAG}.tar.gz"
cd "cactus-bin-${REL_TAG}"


. /local/env/envpython-3.9.5.sh
virtualenv -p python3.9.5 cactus_env

echo "export PATH=$(pwd)/bin:\$PATH" >> cactus_env/bin/activate
echo "export PYTHONPATH=$(pwd)/lib:\$PYTHONPATH" >> cactus_env/bin/activate
source cactus_env/bin/activate
python3 -m pip install -U setuptools pip==21.3.1
python3 -m pip install -U -r ./toil-requirement.txt
python3 -m pip install -U .