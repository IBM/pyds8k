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
Host Volume Mapping interface.
"""

from .common.base import Base, BaseManager
from .common.types import DS8K_VOLMAP
from .volumes import Volume, VolumeManager


class Volmap(Base):
    id_field = 'lunid'
    _template = {'lunid': '',
                 'volume': '',
                 }
    related_resource = {'_volume': (Volume, VolumeManager),
                        }

    def __repr__(self):
        return "<Host Volume Mapping: {0}>".format(self._get_id())


class VolmapManager(BaseManager):
    """
    Manage Host Volume Mapping resources.
    """
    resource_class = Volmap
    resource_type = DS8K_VOLMAP

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(resource_id=resource_id, url=url,
                         obj_class=obj_class, **kwargs)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)

    def posta(self, url='', body=None):
        return self._posta(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)


RESOURCE_TUPLE = (Volmap, VolmapManager)
