#!/bin/bash
set -x
sudo yum -y group install "Development Tools"
sudo wget https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-3.1.2.tar.gz
sudo tar xzf openmpi-3.1.2.tar.gz
cd openmpi-3.1.2
sudo ./configure --prefix=/mnt/software/openmpi/3.1.2
sudo make
sudo make all install
echo "export PATH='$PATH:/mnt/software/openmpi/3.1.2/bin'" >> /users/root/.bashrc
echo "export LD_LIBRARY_PATH='$LD_LIBRARY_PATH:/opt/openmpi/3.1.2/lib/'" >> users/root/.bashrc
cd ..
sudo rm -Rf openmpi-3.1.2
sudo rm -Rf openmpi-3.1.2.tar.gz
