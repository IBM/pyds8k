"""
Usage examples of the DS8000 Python Client.
"""

from pyds8k.client.ds8k.v1.client import Client

# Connect to storage array through HTTPS
# Option verify is passed to requests.
#   From requests documentation:
#    Note that when verify is set to False, requests will accept any TLS
#    certificate presented by the server, and will ignore hostname mismatches
#    and/or expired certificates, which will make your application vulnerable
#    to man-in-the-middle (MitM) attacks. Setting verify to False may be
#    useful during local development or testing.
# verify=False can be used when the DS8K certificate is self-signed.
restclient = Client('ip_address or fqdn',
                    'username',
                    'password',
                    verify=False
                    )

# Available functions are located in pyds8k/resources/ds8k/v1/common/mixins.py

# Create volumes
vol = restclient.create_volumes(name_col=['volume_name'],
                          cap='capacity_in_GiB',
                          pool='pool_id',
                          tp='none')

# Delete volume 
restclient.delete_volume(vol[0].id)

# Get volume
vol = restclient.get_volumes('vol_id')
print(vol.name)
print(vol.cap)

# Get volumes by lss
lss_vols = restclient.get_volumes_by_lss('lss_number')
for vol in lss_vols:
    print(vol.name)
    print(vol.id)

# Calculate allocated capacity by lss
virtual_total = 0
allocated_total = 0
for vol in lss_vols:
    allocated_total += int(vol.real_cap)
    virtual_total += int(vol.virtual_cap)

print(f'{virtual_total=}')
print(f'{allocated_total=}')

# Get pool
pool = restclient.get_pools('pool_id')
print(vol.name)
print(pool.eserep[0])

# Get all of the pools
pools = restclient.get_pools()
for p in pools:
    print(p.name)

# Get all the volumes
vols = []
for p in pools:
    vols.extend(restclient.get_volumes_by_pool(p.id))

for vol in vols:
    print(vol.name)