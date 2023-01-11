git clone https://github.com/ComparativeGenomicsToolkit/cactus.git --recursive

cd cactus
virtualenv -p python3.7 cactus_env
echo "export PATH=$(pwd)/bin:\$PATH" >> cactus_env/bin/activate
echo "export PYTHONPATH=$(pwd)/lib:\$PYTHONPATH" >> cactus_env/bin/activate
source cactus_env/bin/activate
python3.7 -m pip install -U setuptools pip
python3.7 -m pip install -U -r ./toil-requirement.txt
python3.7 -m pip install -U .
grep apt-get Dockerfile | head -1 | sed -e 's/RUN //g' -e 's/apt-get/sudo apt-get/g'
make -j 8
build-tools/downloadPangenomeTools