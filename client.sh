set -x
sudo yum -y install nfs-utils nfs-utils-lib
sudo yum -y install portmap

sudo service nfs start
systemctl enable nfs-server

/etc/init.d/portmap start
/etc/init.d/nfs start
sudo chkconfig --level 35 portmap on
sudo chkconfig --level 35 nfs on

sudo mkdir /software
sudo mkdir /scratch
sudo chmod 777 /software
sudo chmod 777 /scratch




sudo mount -t nfs 192.168.1.1:/software /software
sudo mount -t nfs 192.168.1.3:/scratch /scratch
echo "192.168.1.1:/software /software  nfs defaults 0 0" >> /etc/fstab
echo "192.168.1.3:/scratch /scratch  nfs defaults 0 0" >> /etc/fstab

echo "export PATH='$PATH:/software/openmpi/3.1.2/bin'" >> /users/al844976/.bashrc
echo "export LD_LIBRARY_PATH='$LD_LIBRARY_PATH:/software/openmpi/3.1.2/lib/'" >> /users/al844976/.bashrc
