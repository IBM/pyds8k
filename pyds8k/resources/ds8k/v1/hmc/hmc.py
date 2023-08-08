##############################################################################
# Copyright 2023 IBM Corp.
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
Hardware Management Console interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta

from ..common.base import Base, BaseManager
from ..common.types import DS8K_HMC


@six.add_metaclass(ResourceMeta)
class HMC(Base):
    resource_type = DS8K_HMC

    # id_field = ''

    # _template = {}

    # readonly_fields = {''}

    # related_resources_collection = ()

    # def __repr__(self):
    #     return "<HMC: {0}>".format(self.id)


@six.add_metaclass(ManagerMeta)
class HMCManager(BaseManager):
    """
    Manage Hardware Management Console resources.
    """
    resource_class = HMC
    resource_type = DS8K_HMC
