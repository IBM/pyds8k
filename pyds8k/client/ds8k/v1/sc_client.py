##############################################################################
# Copyright 2019 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

from .client import Client
from pyds8k.utils import dictionarize
from pyds8k.exceptions import NotFound
from logging import getLogger
from pyds8k import PYDS8K_DEFAULT_LOGGER

logger = getLogger(PYDS8K_DEFAULT_LOGGER)


class SCClient(object):
    """
    SC side client. Used to interaction with current side client.

    !--important: the id field of all resources are case insensitive--!
    """

    def __init__(self, service_address, user, password,
                 port=None,
                 hostname='',
                 ):
        self.client = Client(service_address, user, password,
                             port=port,
                             hostname=hostname,
                             )

    @dictionarize
    def get_system(self):
        return self.client.get_system()

    @dictionarize
    def get_volume(self, volume_id):
        return self.client.get_volumes(volume_id)

    @dictionarize
    def get_host(self, host_name):
        return self.client.get_hosts(host_name)

    @dictionarize
    def get_extentpool(self, pool_id):
        pool = self.client.get_pools(pool_id)
        try:
            # lazy-loading
            eserep = pool.eserep[0]
            pool.representation['eserep'] = eserep.representation
        except AttributeError:
            pass
        return pool

    @dictionarize
    def list_extentpools(self):
        """
        return extent pool list without ese capacity info.
        """
        return self.client.get_pools()

    @dictionarize
    def list_hosts(self):
        return self.client.get_hosts()

    @dictionarize
    def list_extentpool_volumes(self, pool_id):
        # two requests
        # pool = self.client.get_pools(pool_id)
        # return pool.volumes

        # one request
        return self.client.get_volumes_by_pool(pool_id)

    @dictionarize
    def list_extentpool_virtualpool(self, pool_id):
        return self.client.get_eserep_by_pool(pool_id)

    @dictionarize
    def list_flashcopies(self):
        return self.client.get_flashcopies()

    @dictionarize
    def list_volume_flashcopies(self, volume_id):
        # two requests
        # volume = self.client.get_volumes(volume_id)
        # return volume.flashcopy

        # one request
        return self.client.get_flashcopies_by_volume(volume_id)

    @dictionarize
    def list_remotecopies(self):
        return self.client.get_pprc()

    @dictionarize
    def list_volume_remotecopies(self, volume_id):
        return self.client.get_pprc_by_volume(volume_id)

    @dictionarize
    def list_logical_subsystems(self):
        return self.client.get_lss()

    @dictionarize
    def list_lss_volumes(self, lss_number):
        return self.client.get_volumes_by_lss(lss_number)

    @dictionarize
    def list_fcports(self):
        return self.client.get_ioports()

    def list_ioenclosures(self):
        pass

    def get_client_descriptor(self):
        pass

    def list_known_wwpns(self):
        pass

    def get_used_lun_numbers_by_host(self, host_name):
        mappings = self.client.get_mappings_by_host(host_name)
        return [mapping.id for mapping in mappings]

    def create_volumes(self, pool_id, capacity_in_GiB, sam,
                       volume_names_list):
        return self.client.create_volumes(name_col=volume_names_list,
                                          cap=capacity_in_GiB,
                                          pool=pool_id,
                                          tp=sam)

    def rename_volume(self, volume_id, new_name):
        return self.client.update_volume_rename(volume_id=volume_id,
                                                new_name=new_name)

    def extend_volume(self, volume_id, new_size_in_GiB):
        return self.client.update_volume_extend(volume_id=volume_id,
                                                new_size=new_size_in_GiB,
                                                captype='gib')

    def delete_volume(self, volume_id):
        # remember to unmap all hosts before delete.
        return self.client.delete_volume(volume_id=volume_id)

    def relocate_volume(self, volume_id, new_pool_id):
        return self.client.update_volume_move(volume_id=volume_id,
                                              new_pool=new_pool_id)

    def create_extentpool_virtualpool(self):
        pass

    def remove_extentpool_virtualpool(self):
        pass

    def crate_host(self, host_name, wwpn, host_type='VMware'):
        hosts = self.client.create_host(host_name=host_name,
                                        hosttype=host_type
                                        )
        self.attach_hostport_to_host(host_name=hosts[0].id, wwpn=wwpn)
        return hosts[0].id

    def delete_host(self, host_name):
        # delete a host will delete all the attached host ports.
        return self.client.delete_host(host_name=host_name)

    def attach_hostport_to_host(self, host_name, wwpn):
        return self._get_attach_or_create_host_port(host_name=host_name,
                                                    wwpn=wwpn
                                                    )

    def detach_hostport_from_host(self, wwpn):
        return self.client.delete_host_port(port_id=wwpn)

    def map_volume_to_host(self, host_name, volume_id, lunid):
        return self.client.map_volume_to_host(host_name=host_name,
                                              volume_id=volume_id,
                                              lunid=lunid
                                              )

    def unmap_volume_from_host(self, host_name, lunid):
        return self.client.unmap_volume_from_host(host_name=host_name,
                                                  lunid=lunid
                                                  )

    def _get_attach_or_create_host_port(self, host_name, wwpn):
        try:
            host_port = self.client.get_host_port(port_id=wwpn)
            return self.client.update_host_port_change_host(
                port_id=host_port.id,
                host_name=host_name
            )
        except NotFound:
            logger.debug(
                'host port {} is not found, creating new...'.format(wwpn)
            )
            return self.client.create_host_port(port_id=wwpn,
                                                host_name=host_name
                                                )

    # APIs below are deprecated.

    # def list_cached_systems(self):
    #    pass

    def list_volume_groups(self):
        pass

    def get_volume_group(self):
        pass

    def attach_volume_group(self):
        pass

    def detach_volume_group(self):
        pass

    def add_volumes_to_volgrp(self):
        pass

    def remove_volume_from_volgrp(self):
        pass

    def create_volume_group(self):
        pass

    def remove_volume_group(self):
        pass

    def list_scsi_host_ports(self):
        pass

    def get_scsi_host_port(self):
        pass

    def remove_scsi_host_port(self):
        pass

    def create_scsi_host_port(self):
        pass
