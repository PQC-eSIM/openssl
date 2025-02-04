#install liboqs
sudo apt install -y astyle cmake gcc libtool libssl-dev make ninja-build libssl-dev python3-pytest python3-pytest-xdist unzip xsltproc doxygen graphviz python3-yaml valgrind

cd $PWD
sudo rm -r liboqs

git clone https://github.com/open-quantum-safe/liboqs.git

OPENSSL_DIR=$PWD
cd liboqs
mkdir build && cd build
cmake -GNinja -DOQS_USE_OPENSSL=ON ..
#cmake -GNinja -DBUILD_SHARED_LIBS=ON .. # LibOQS errors
cmake -GNinja -DCMAKE_INSTALL_PREFIX=$OPENSSL_DIR/oqs ..
ninja
sudo ninja install 

#install openssl
cd $OPENSSL_DIR
# ./Configure no-shared linux-x86_64 -lm
# ./Configure no-shared linux-aarch64 -lm
ARCH=$(uname -m)
./Configure no-shared linux-$ARCH -lm

# Dynamically set the number of jobs to the number of processors
sudo make -j$(nproc)
