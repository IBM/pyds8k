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
User interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta
from .common.types import DS8K_USER
from .common.base import Base, ReadOnlyManager


@six.add_metaclass(ResourceMeta)
class User(Base):
    resource_type = DS8K_USER
    id_field = 'name'
    _template = {'name': '',
                 'state': '',  # locked|active
                 'group': [],
                 }


@six.add_metaclass(ManagerMeta)
class UserManager(ReadOnlyManager):
    """
    Manage User resources.
    """
    resource_class = User
    resource_type = DS8K_USER
