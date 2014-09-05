#!/usr/bin/env python
import json
import requests

auth_url = 'http://172.16.18.1:5000/v2.0/tokens'
# Please Change the value of the tenantName to your tenant name.
tenant_name = ""
# Please Change the values of username and password for your user account.
user_name = ""
password = ""
# Plesse change XXXXX to the name of VM that floatingIP address you want to get.
vm_name = "XXXXX"

data = json.dumps({"auth": {"tenantName": tenant_name, "passwordCredentials": {"username": user_name, "password": password}}})
headers = {"Content-Type": "application/json", "Accept": "application/json"}

r = requests.post(auth_url, data=data, headers=headers)
content = json.loads(r.content)['access']
r.close
for url_info in content['serviceCatalog']:
    if url_info['name'] == 'nova':
        get_url = url_info['endpoints'][0]['publicURL'] + '/servers'
        break
auth_token = json.loads(r.content)['access']['token']['id']

headers = {"X-Auth-Token": auth_token, "Accept": "application/json"}
r = requests.get(get_url, headers=headers)
content = json.loads(r.content)['servers']
r.close
for server_info in content:
    if server_info['name'] == vm_name:
        for link in server_info['links']:
            if link['rel'] == "self":
                details_url = link['href']
        break

floating_ip = None
headers = {"X-Auth-Token": auth_token, "Accept": "application/json"}
r = requests.get(details_url, headers=headers)
content = json.loads(r.content)['server']
r.close
net_info = content['addresses'].values()[0]
for info in net_info:
    if info['OS-EXT-IPS:type'] == "floating":
        floating_ip = info['addr']
        break
print floating_ip
