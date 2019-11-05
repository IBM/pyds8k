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
Event interface.
"""

from .common.types import DS8K_EVENT
from .common.base import Base, ReadOnlyManager


class Event(Base):
    # id_field = 'id'
    _template = {'id': '',
                 'type': '',
                 'severity': '',
                 'time': '',
                 'resource_id': '',
                 'formatted_parameter': '',
                 'description': '',
                 }


class EventManager(ReadOnlyManager):
    """
    Manage Event resources.
    """
    resource_class = Event
    resource_type = DS8K_EVENT


RESOURCE_TUPLE = (Event, EventManager)
