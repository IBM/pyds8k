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
advanced FlashCopies interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta
from ..common.base import Base, BaseManager
from ..common.types import DS8K_CS_FLASHCOPY, DS8K_FLASHCOPY
from ..volumes import Volume, VolumeManager


@six.add_metaclass(ResourceMeta)
class FlashCopy(Base):
    resource_type = DS8K_CS_FLASHCOPY
    _template = {'id': None,
                 'persistent': None,
                 'recording': None,
                 'backgroundcopy': None,
                 'state': None,
                 'options': [],
                 'volume_pairs': []
                 }

    related_resource = {'_volume_pairs': [{
        'source_volume': (Volume, VolumeManager),
        'target_volume': (Volume, VolumeManager)
    }]
    }

    def __repr__(self):
        return "<FlashCopy: {0}>".format(self._get_id())

    def _add_details(self, info, force=False):
        super(FlashCopy, self)._add_details(info, force=force)
        if DS8K_FLASHCOPY in info:
            self._id = info[DS8K_FLASHCOPY][0]['id']


@six.add_metaclass(ManagerMeta)
class FlashCopyManager(BaseManager):
    """
    Manage advanced FlashCopies resources.
    """
    resource_class = FlashCopy
    resource_type = DS8K_CS_FLASHCOPY

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(resource_id=resource_id, url=url,
                         obj_class=obj_class, **kwargs)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)

    def posta(self, url='', body=None):
        return self._posta(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)
