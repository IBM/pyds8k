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
Host Ports interface.
"""
from .common.types import DS8K_HOST_PORT
from .common.base import Base, BaseManager
from .hosts import Host, HostManager
from .ioports import IOPort, IOPortManager


class HostPort(Base):
    id_field = 'wwpn'
    _template = {'wwpn': '',
                 'state': None,
                 'hosttype': None,
                 'addrdiscovery': None,
                 'lbs': None,
                 'host': '',
                 'login_type': None,
                 'logical_path_established': None,
                 'wwnn': None,
                 'login_ports': None,
                 }
    related_resource = {'_host': (Host, HostManager),
                        }
    readonly_fileds = ('state', 'hosttype', 'addrdiscovery', 'lbs',)

    def _add_details(self, info, force=False):
        super(HostPort, self)._add_details(info, force=force)
        self._start_updating()
        self._set_ioports()
        self._stop_updating()

    def _set_ioports(self):
        OCCUPIED_IOPORTS = 'login_ports'
        port_list = self.representation.get(OCCUPIED_IOPORTS, [])
        port_obj_list = []
        for port in port_list:
            port_obj = IOPort(self.client,
                              manager=IOPortManager(self.client),
                              info=port,
                              loaded=False,
                              )
            port_obj_list.append(port_obj)
        self.representation[OCCUPIED_IOPORTS] = [p.id for p in port_obj_list]
        setattr(self, OCCUPIED_IOPORTS, port_obj_list)

    # def __repr__(self):
    #    return "<HostPort: {0}>".format(self.id)


class HostPortManager(BaseManager):
    """
    Manage Host Ports resources.
    """
    resource_class = HostPort
    resource_type = DS8K_HOST_PORT

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


RESOURCE_TUPLE = (HostPort, HostPortManager)
