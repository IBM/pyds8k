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
LSS interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta
from .common.types import DS8K_LSS, DS8K_VOLUME, \
    DS8K_LCU_TYPES, \
    DS8K_LSS_TYPES, \
    DS8K_LCU_TYPE_3990_6, \
    DS8K_VOLUME_TYPE_CKD
from .common.base import Base, BaseManager
from .common.mixins import VolumeMixin


@six.add_metaclass(ResourceMeta)
class LSS(VolumeMixin, Base):
    resource_type = DS8K_LSS
    # id_field = 'id'
    _template = {
        'id': '',
        'type': '',
        'ckd_base_cu_type': '',
        'group': '',
        'addrgrp': '',
        'sub_system_identifier': '',
        'configvols': '',
        DS8K_VOLUME: '',
    }

    ckd_template = _template.copy()
    ckd_template.update(
        {
            'ckd_base_cu_type': DS8K_LCU_TYPE_3990_6,
            # lss type shared with volume type
            'type': DS8K_VOLUME_TYPE_CKD
        }
    )
    template_dict = {
        DS8K_VOLUME_TYPE_CKD: ckd_template
    }

    readonly_fileds = ()
    related_resource = {}
    related_resources_collection = (DS8K_VOLUME, )

    def __init__(
            self,
            client,
            manager=None,
            url='',
            info=None,
            resource_id=None,
            parent=None,
            loaded=False,
            lss_type=DS8K_VOLUME_TYPE_CKD,
            lcu_type=DS8K_LCU_TYPE_3990_6
    ):
        super(LSS, self).__init__(
            client,
            manager=manager,
            url=url,
            info=info,
            resource_id=resource_id,
            parent=parent,
            loaded=loaded
        )
        self._lss_type = lss_type
        self._lcu_type = lcu_type
        # isolated to ckd only
        self._verify_type(self._lss_type, DS8K_LSS_TYPES)
        self._verify_type(self._lcu_type, DS8K_LCU_TYPES)
        self._template = self.template_dict[self._lss_type]

    def __repr__(self):
        return "<Storage LSS: {0}>".format(self._get_id())


@six.add_metaclass(ManagerMeta)
class LSSManager(BaseManager):
    """
    Manage LSS resources.
    """
    resource_class = LSS
    resource_type = DS8K_LSS

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

    def delete(self, url=''):
        return self._delete(url=url)
