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
Storage system interface.
"""
from .common.types import DS8K_SYSTEM
from .common.base import Base, ReadOnlyManager


class System(Base):
    id_field = 'id'
    _template = {'id': '',
                 'name': '',
                 'state': '',
                 'release': '',
                 'bundle': '',
                 'MTM': '',
                 'sn': '',
                 'wwnn': '',
                 'cap': '',
                 'capalloc': '',
                 'capavail': '',
                 'capraw': '',
                 }

    def __repr__(self):
        return "<Storage System: {0}>".format(self.id)

    def get_system(self):
        return self.get_systems()[0]


class SystemManager(ReadOnlyManager):
    """
    Manage Storage System resources.
    """
    resource_class = System
    resource_type = DS8K_SYSTEM


RESOURCE_TUPLE = (System, SystemManager)
