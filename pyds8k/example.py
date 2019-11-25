"""
Usage examples of the DS8000 Python Client.
"""

from pyds8k.client.ds8k.v1.client import Client

# Connect storage array through SSH
restclient = Client(service_address='ip_address', user='username',
                    password='password')

# Create volumes
restclient.create_volumes(name_col=["volume_name"],
                          cap="capacity_in_GiB",
                          pool="pool_id",
                          tp="none")

# Get Volume from storage
vol = restclient.get_volumes('vol_id')
print(vol['name'])

# Get all the volume from storage by lss
lss_vols = restclient.get_volumes_by_lss('lss_number')
for vol in lss_vols:
    print(vol['name'])

# Get all the volumes from storage
vols = restclient.get_volumes()
for vol in vols:
    print(vol['name'])

# Get Pool from storage
pool = restclient.get_pools('pool_id')
print(pool['name'])
print(pool.eserep[0])

# Getting all of the pools from storage
pools = restclient.get_pools()
for p in pools:
    print(p['name'])
