set -x
sudo yum -y install nfs-utils nfs-utils-lib

sudo mkdir -p /users/al844976/software
sudo chmod 777 /users/al844976/software

sudo mkdir -p /scratch
sudo chmod 777 /scratch

sudo systemctl enable nfs-server
sudo service nfs start

sudo mount -t nfs 192.168.1.1:/software /users/al844976/software
sudo mount -t nfs 192.168.1.3:/scratch /scratch

echo '192.168.1.1:/software /users/al844976/software  nfs defaults 0 0' >> /etc/fstab
echo '192.168.1.3:/scratch /scratch  nfs defaults 0 0' >> /etc/fstab

echo "export PATH='$PATH:/software/openmpi/3.1.2/bin'" >> /users/al844976/.bashrc
echo "export LD_LIBRARY_PATH='$LD_LIBRARY_PATH:/software/openmpi/3.1.2/lib/'" >> /users/al844976/.bashrc
