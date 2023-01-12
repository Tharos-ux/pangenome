tar -xzf "cactus-bin-${REL_TAG}.tar.gz"
cd "cactus-bin-${REL_TAG}"

virtualenv -p python3.9 cactus_env
echo "export PATH=$(pwd)/bin:\$PATH" >> cactus_env/bin/activate
echo "export PYTHONPATH=$(pwd)/lib:\$PYTHONPATH" >> cactus_env/bin/activate
source cactus_env/bin/activate
python3 -m pip install -U setuptools pip
python3 -m pip install -U -r ./toil-requirement.txt
python3 -m pip install -U .
cd bin && for i in wigToBigWig faToTwoBit bedToBigBed bigBedToBed bedSort hgGcPercent; do wget -q http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/${i}; chmod ugo+x ${i}; done