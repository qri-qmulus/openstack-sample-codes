#!/usr/bin/env python
import os
# Please Check if novaclient was installed
import novaclient.v1_1.client as nvclient
# Please Export Environment Variables first
from credentials import get_nova_creds

# Name of your Instance(VM) of the searching floating IP.
vm_name = "flx-XXXXX-test"

floating_ip = None
# Get credentials from environment variables.
creds = get_nova_creds()
nova = nvclient.Client(**creds)
# Get detail information of this VM
server = nova.servers.find(name=vm_name)
# Get we only get network information from server detail information.
for addr_info in server.addresses.values()[0]:
    # Get floating IP type from netwrok information
    if 'floating' == addr_info['OS-EXT-IPS:type']:
        floating_ip = addr_info['addr']
        break
print floating_ip
