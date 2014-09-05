#!/usr/bin/env python
import os
import sys
# Please Check if novaclient was installed
import novaclient.v1_1.client as nvclient

auth_url = 'http://IaaS_URL:5000/v2.0'
# Tenant name for the user.
project_id = 'Future-CSRC'
# User name who crearted the searching VM
username = 'xxx_XMen'
# Password of username
api_key = 'IamXMen'
# Name of your Instance(VM) of the searching floating IP.
vm_name = 'Home_of_XMen'

floating_ip = None
nova = nvclient.Client(auth_url=auth_url, username=username,
                       api_key=api_key, project_id=project_id)
# Get detail information of this VM
server = nova.servers.find(name=vm_name)
# Get we only get network information from server detail information.
for addr_info in server.addresses.values()[0]:
    # Get floating IP type from netwrok information
    if 'floating' == addr_info['OS-EXT-IPS:type']:
        floating_ip = addr_info['addr']
        break
print floating_ip
