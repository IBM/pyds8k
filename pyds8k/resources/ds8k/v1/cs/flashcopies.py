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
FlashCopies interface.
"""
from pyds8k.base import ManagerMeta, ResourceMeta
from ..common.base import Base, BaseManager
from ..common.types import DS8K_FLASHCOPIES, DS8K_HOST
from ..hosts import Host, HostManager
from ..volumes import Volume, VolumeManager


class FlashCopy(Base, metaclass=ResourceMeta):
    resource_type = DS8K_FLASHCOPIES
    _template = {'id': None,
                 'persistent': None,
                 'recording': None,
                 'backgroundcopy': None,
                 'state': None,
                 'options': [],
                 'volume_pairs': []
                 }

    related_resource = {'sourcevolume': (Volume, VolumeManager),
                        'targetvolume': (Volume, VolumeManager)
                        }

    def __init__(self, client, manager=None, url='', info={},
                 resource_id=None,
                 parent=None,
                 loaded=False,
                 ):
        super(FlashCopy, self).__init__(client,
                                        manager=manager,
                                        url=url,
                                        info=info,
                                        resource_id=resource_id,
                                        parent=parent,
                                        loaded=loaded,
                                        )

    def __repr__(self):
        return "<FlashCopy: {0}>".format(self._get_id())

    def _add_details(self, info, force=False):
        super(FlashCopy, self)._add_details(info, force=force)

        # import pdb
        # pdb.set_trace()
        # Temporarily, remove this line when flashcopy resource has id field.
        self._id = '{}:{}'.format(
            info['volume_pairs'][0]['source_volume'],
            info['volume_pairs'][0]['target_volume']
        )

    def __repr__(self):
        return "<FlashCopy: {}>".format(self.id)

    def _set_hosts(self):
        host_list = self.representation.get('host', [])
        if host_list:
            host_obj_list = []
            for host in host_list:
                host_obj = Host(self.client,
                                manager=HostManager(self.client),
                                info=host,
                                loaded=False,
                                )
                host_obj_list.append(host_obj)
            self.representation[DS8K_HOST] = [
                h.host_id for h in host_obj_list]
            setattr(self, DS8K_HOST, host_obj_list)


class FlashCopyManager(BaseManager, metaclass=ManagerMeta):
    """
    Manage FlashCopies resources.
    """
    resource_class = FlashCopy
    resource_type = DS8K_FLASHCOPIES

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(resource_id=resource_id, url=url,
                         obj_class=obj_class, **kwargs)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)

    def posta(self, url='', body=None):
        return self._posta(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)
