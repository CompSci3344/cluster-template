# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


tourDescription = \
"""
This profile provides the template for a full research cluster with head node, scheduler, compute nodes, and shared file systems.
First node (head) should contain: 
- Shared home directory using Networked File System
- Management server for SLURM
Second node (metadata) should contain:
- Metadata server for SLURM
Third node (storage):
- Shared software directory (/software) using Networked File System
Remaining three nodes (computing):
- Compute nodes  
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

prefixForIP = "192.168.1."

link = request.LAN("lan")

for i in range(0,6):
  if i == 0:
    node = request.XenVM("head")
    node.routable_control_ip = "true"
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/setupNFS_head.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/setupNFS_head.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/passwordless.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
    
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /users/al844976/scratch"))
  elif i == 1:
    node = request.XenVM("metadata")
  elif i == 2:
    node = request.XenVM("storage")
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/setupNFS_Storage.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/setupNFS_Storage.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
  else:
    node = request.XenVM("compute-" + str(i-2))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/client.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/client.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
    #node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/setupNFS_Storage.sh"))
    #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/setupNFS_Storage.sh"))
    #node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/mountStorage.sh"))
    #node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mountStorage.sh"))
    
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  node.cores = 4
  node.ram = 4096
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  if i != 0:
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/passwordless.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
  
  
  # This code segment is added per Benjamin Walker's solution to address the StrictHostKeyCheck issue of ssh
  #node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/ssh_setup.sh"))
  #node.addService(pg.Execute(shell="sh", command="sudo -H -u al844976 bash -c '/local/repository/ssh_setup.sh'"))

  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
