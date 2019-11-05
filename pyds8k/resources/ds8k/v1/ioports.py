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
IO Ports interface.
"""
from .common.types import DS8K_IOPORT
from .common.base import Base, ReadOnlyManager
from .io_enclosures import IOEnclosure, IOEnclosureManager


class IOPort(Base):
    # id_field = 'id'
    _template = {'id': '',
                 'state': '',
                 'protocol': '',
                 'wwpn': '',
                 'type': '',
                 'speed': '',
                 'loc': '',
                 'io_enclosure': '',
                 }

    related_resource = {'_io_enclosure': (IOEnclosure, IOEnclosureManager),
                        }

    # def __repr__(self):
    #    return "<FCPort: {0}>".format(self.id)


class IOPortManager(ReadOnlyManager):
    """
    Manage IO Ports resources.
    """
    resource_class = IOPort
    resource_type = DS8K_IOPORT


RESOURCE_TUPLE = (IOPort, IOPortManager)
