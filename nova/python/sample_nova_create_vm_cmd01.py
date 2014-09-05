#!/usr/bin/env python
import os
import sys
import time
# Please Check if novaclient was installed.
try:
    import novaclient.v1_1.client as nvclient
except:
    print('Please install Nova client first.')
    sys.exit(1)

# The QMULUS access URL.
auth_url = 'https://172.16.17.1:5000/v2.0'
# Tenant name for the user.
project_id = 'myproject'
# User name who crearted the searching VM
username = 'demo'
# Password of username.
api_key = 'demo'
# SSL Key to communicate with QMULUS.
cacert = '/home/ubuntu/arcus_ca.pem'
# Name of your Instance(VM) to be created.
vm_name = 'demo-vm'
# Image Name to create the Instance.
image_name = 'ubuntu_12.04-pwd'
# Network Name to be used by the Instance of the user Tenant.
network_name = 'net_demo'
# Flavor of the creating Instance.
flavor_name = 'm1.small'
# KeyPair Name
keypair_name = 'my_keypair'
# Floating IP pool name
fip_pool_name = 'net_external'


# Create a nova client.
nova = nvclient.Client(auth_url=auth_url, username=username,
                       api_key=api_key, project_id=project_id,
                       cacert=cacert)

# Get information of all images.
#nova_images = nova.images.list()
# Get information of all networks of the tenant.
#nova_networks = nova.networks.list()
# Get information of all flavors.
#nova_flavors = nova.flavors.list()

# Get ID of the image.
image = nova.images.find(name=image_name)
image_id = image.id
image_resp_name = image.name
# Get ID of the network.
net = nova.networks.find(label=network_name)
net_id = net.id
net_resp_name = net.label
# Get ID of the flavor.
flavor = nova.flavors.find(name=flavor_name)
flavor_id = flavor.id
flavor_resp_name = flavor.name

# Allocate a new Floating IP address.
new_fip = nova.floating_ips.create(pool=fip_pool_name)

"""
# List all floating IP and you can choose a free one to assocaite.
fip_list = nova.floating_ips.list()
for fip in fip_list:
    print '-' * 100
    print fip.id
    print fip.ip
    print("instance_id : %s" % fip.instance_id)
    print("pool : %s" % fip.pool)
"""

# Start to create an instance.
nics = [{'net-id': net_id}]
instance = nova.servers.create(name=vm_name, image=image,
                               flavor=flavor, nics=nics)
# If you want to use Key to access your instance.
                               #, key_name=keypair_name)

# Check if instance is created and ok.
time.sleep(10)
# Make Sure name is Unique or use id for search.
server = nova.servers.find(name=vm_name)
print('Instance: %s, status: %s' % (vm_name, str(server.status)))

# Assocaite floating ip to the Instance.
nova.servers.add_floating_ip(server, new_fip.ip)

time.sleep(5)

# Delete the Instance.
server.delete()

time.sleep(5)

# Delete the Allocated floating IP
nova.floating_ips.delete(new_fip.id)
