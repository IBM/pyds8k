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
import six
from pyds8k.base import ManagerMeta, ResourceMeta

from .common.base import Base, ReadOnlyManager
from .common.types import DS8K_ENCRYPTION_GROUP


@six.add_metaclass(ResourceMeta)
class EncryptionGroup(Base):
    resource_type = DS8K_ENCRYPTION_GROUP
    # id_field = 'id'
    _template = {'id': '',
                 'state': '',
                 }


@six.add_metaclass(ManagerMeta)
class EncryptionGroupManager(ReadOnlyManager):
    """
    Manage Encryption Group resources.
    """
    resource_class = EncryptionGroup
    resource_type = DS8K_ENCRYPTION_GROUP
