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
Storage volume interface.
"""

from .common.base import Base, BaseManager
from .common import types
from .pools import Pool, PoolManager
from .lss import LSS, LSSManager
from .hosts import Host, HostManager


class Volume(Base):
    # id_field = 'id'

    # Set the value to None if the field is not required when creation.
    _template = {'id': None,
                 'name': '',
                 'state': '',
                 'cap': '',
                 'real_cap': None,
                 'virtual_cap': None,
                 'captype': '',
                 'stgtype': '',
                 'VOLSER': None,
                 'allocmethod': '',
                 'tp': '',
                 'capalloc': '',
                 'MTM': None,
                 'datatype': '',
                 'easytier': '',
                 'tieralloc': [],
                 'lss': '',
                 'pool': '',
                 types.DS8K_HOST: None,
                 types.DS8K_FLASHCOPY: None,
                 types.DS8K_PPRC: None,
                 }
    fb_template = _template.copy()
    fb_template.update({'stgtype': types.DS8K_VOLUME_TYPE_FB})

    ckd_template = _template.copy()
    ckd_template.update({'stgtype': types.DS8K_VOLUME_TYPE_FB})

    template_dict = {types.DS8K_VOLUME_TYPE_FB: fb_template,
                     types.DS8K_VOLUME_TYPE_CKD: ckd_template,
                     }
    readonly_fileds = ('state', 'stgtype', 'VOLSER', 'allocmethod', 'tp',
                       'capalloc', 'MTM', 'datatype', 'easytier', 'tieralloc',
                       'lss'
                       )
    related_resource = {'_pool': (Pool, PoolManager),
                        '_lss': (LSS, LSSManager)
                        }
    related_resources_collection = (types.DS8K_HOST,
                                    types.DS8K_FLASHCOPY,
                                    types.DS8K_PPRC)

    def __init__(self, client, manager=None, url='', info={},
                 resource_id=None,
                 parent=None,
                 loaded=False,
                 volume_type=types.DS8K_VOLUME_TYPE_FB,
                 ):
        super(Volume, self).__init__(client,
                                     manager=manager,
                                     url=url,
                                     info=info,
                                     resource_id=resource_id,
                                     parent=parent,
                                     loaded=loaded,
                                     )
        self.volume_type = volume_type
        self._verify_volume_type()
        self._template = self.get_template_from_volume_type(volume_type)

    def __repr__(self):
        return "<Storage Volume: {0}>".format(self._get_id())

    def get_template_from_volume_type(self, volume_type):
        return self.template_dict[volume_type]

    def _verify_volume_type(self):
        self._verify_type(self.volume_type, types.DS8K_VOLUME_TYPES)

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
            self.representation[types.DS8K_HOST] = [
                h.host_id for h in host_obj_list]
            setattr(self, types.DS8K_HOST, host_obj_list)

    def _add_details(self, info, force=False):
        super(Volume, self)._add_details(info, force=force)
        self._start_updating()
        self._set_hosts()
        self._stop_updating()


class VolumeManager(BaseManager):
    """
    Manage Storage Volume resources.
    """
    resource_class = Volume
    resource_type = types.DS8K_VOLUME

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(resource_id=resource_id, url=url,
                         obj_class=obj_class, **kwargs)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)

    # def post(self, url='', body=None):
    #    return self._post(url, body)

    def posta(self, url='', body=None):
        return self._posta(url=url, body=body)

    def put(self, url='', body=None):
        return self._put(url=url, body=body)

    def patch(self, url='', body=None):
        return self._patch(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)


RESOURCE_TUPLE = (Volume, VolumeManager)
