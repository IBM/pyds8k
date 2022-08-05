##############################################################################
# Copyright 2022 IBM Corp.
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
Resource Group interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta

from .common.base import Base, BaseManager
from .common.types import DS8K_RESOURCE_GROUP


@six.add_metaclass(ResourceMeta)
class ResourceGroup(Base):
    resource_type = DS8K_RESOURCE_GROUP
    # id_field = 'id'

    _template = {
        'id': '',
        'name': '',
        'state': '',
        'label': '',
        'cs_global': '',
        'pass_global': '',
        'gm_masters': '',
        'gm_sessions': '',
    }


@six.add_metaclass(ManagerMeta)
class ResourceGroupManager(BaseManager):
    """
    Manage Resource Group resources.
    """
    resource_class = ResourceGroup
    resource_type = DS8K_RESOURCE_GROUP

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(
            resource_id=resource_id,
            url=url,
            obj_class=obj_class,
            **kwargs
        )

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(
            url=url,
            obj_class=obj_class,
            body=body,
            **kwargs
        )

    def posta(self, url='', body=None):
        return self._posta(url=url, body=body)

    def put(self, url='', body=None):
        return self._put(url=url, body=body)

    def patch(self, url='', body=None):
        # patch doesn't remove keys with empty values, override
        if body:
            body = self.remove_empty_key_values_from_dict(body)
        return self._patch(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)

    def remove_empty_key_values_from_dict(self, input_dict):
        return {k: v for k, v in input_dict.items() if v}
