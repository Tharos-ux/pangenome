 git clone https://github.com/ComparativeGenomicsToolkit/hal.git

 mkdir DIR/hdf5
 wget http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.1/src/hdf5-1.10.1.tar.gz
 tar xzf hdf5-1.10.1.tar.gz
 cd hdf5-1.10.1
 ./configure --enable-cxx --prefix DIR/hdf5
 make && make install

 export PATH=DIR/hdf5/bin:${PATH}
 export h5prefix=-prefix=DIR/hdf5

 cd ..

git clone https://github.com/ComparativeGenomicsToolkit/sonLib.git
pushd sonLib && make && popd

