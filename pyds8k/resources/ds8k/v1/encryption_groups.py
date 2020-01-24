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
Encryption Group interface.
"""
from pyds8k.base import ManagerMeta, ResourceMeta
from .common.types import DS8K_ENCRYPTION_GROUP
from .common.base import Base, ReadOnlyManager


class EncryptionGroup(Base, metaclass=ResourceMeta):
    resource_type = DS8K_ENCRYPTION_GROUP
    # id_field = 'id'
    _template = {'id': '',
                 'state': '',
                 }


class EncryptionGroupManager(ReadOnlyManager, metaclass=ManagerMeta):
    """
    Manage Encryption Group resources.
    """
    resource_class = EncryptionGroup
    resource_type = DS8K_ENCRYPTION_GROUP
