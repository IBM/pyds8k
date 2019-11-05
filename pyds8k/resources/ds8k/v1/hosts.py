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

"""
Host interface.
"""

from .common.base import Base, BaseManager
from .common.mixins import FCPortMixin, HostPortMixin, VolumeMixin, VolmapMixin
from .common import types


class Host(FCPortMixin, HostPortMixin, VolumeMixin, VolmapMixin, Base):
    id_field = 'name'
    alias = {'id': 'host_id'}
    _template = {'name': '',
                 'state': '',
                 'hosttype': '',
                 'addrmode': '',
                 'addrdiscovery': '',
                 'lbs': '',
                 types.DS8K_VOLUME: '',
                 types.DS8K_IOPORT: '',
                 types.DS8K_HOST_PORT: '',
                 }
    readonly_fileds = ('state', 'addrmode', 'addrdiscovery', 'lbs',
                       types.DS8K_HOST_PORT,
                       )
    related_resources_collection = (types.DS8K_VOLUME,
                                    types.DS8K_IOPORT,
                                    types.DS8K_HOST_PORT,
                                    types.DS8K_VOLMAP,
                                    )
    # def __repr__(self):
    #    return "<Host: {0}>".format(self.id)

    def update_host_add_ioports(self, port_ids=[]):
        if not port_ids:
            return self.update_host_add_ioports_all(self.id)
        updated_port_ids = self._update_ioports_and_return_ids(port_ids)

        _, res = self.one(types.DS8K_HOST,
                          self.id,
                          rebuild_url=True
                          ).update({'ioports': updated_port_ids})
        return res

    def update_host_rm_ioports(self, port_ids=[]):
        if not port_ids:
            return self.update_host_rm_ioports_all(self.id)
        updated_port_ids = self._update_ioports_and_return_ids(port_ids, '-')

        _, res = self.one(types.DS8K_HOST,
                          self.id,
                          rebuild_url=True
                          ).update({'ioports': updated_port_ids})
        return res

    def _update_ioports_and_return_ids(self, port_ids, operator='+'):
        ports = []
        if not isinstance(port_ids, list):
            port_ids = [port_ids, ]
        for port_id in port_ids:
            port = port_id
            if not isinstance(port_id, Base):
                port = self.one(types.DS8K_IOPORT, port_id)
            ports.append(port)
        updated = self._update_list_field(types.DS8K_IOPORT, ports, operator)
        return [port.id for port in updated]


class HostManager(BaseManager):
    """
    Manage Host resources.
    """
    resource_class = Host
    resource_type = types.DS8K_HOST

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(resource_id=resource_id,
                         url=url, obj_class=obj_class, **kwargs)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)

    def posta(self, url='', body=None):
        return self._posta(url=url, body=body)

    def put(self, url='', body=None):
        return self._put(url=url, body=body)

    def patch(self, url='', body=None):
        return self._patch(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)


RESOURCE_TUPLE = (Host, HostManager)
