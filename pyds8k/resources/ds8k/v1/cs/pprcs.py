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
advanced PPRC interface.
"""

from ..common.base import Base, ReadOnlyManager
from ..common.types import DS8K_CS_PPRC
from ..volumes import Volume, VolumeManager
from ..systems import System, SystemManager


class CSPPRC(Base):
    base_url = '/api/v1/cs'

    _template = {'id': '',
                 'type': '',
                 'state': '',
                 'source_system': '',
                 'target_system': '',
                 'source_volume': '',
                 'target_volume': '',
                 }

    related_resource = {'_source_volume': (Volume, VolumeManager),
                        '_source_system': (System, SystemManager),
                        '_target_volume': (Volume, VolumeManager),
                        '_target_system': (System, SystemManager),
                        }

    def _add_details(self, info, force=False):
        super(CSPPRC, self)._add_details(info, force=force)


class CSPPRCManager(ReadOnlyManager):
    """
    Manage advanced PPRC resources.
    """
    resource_class = CSPPRC
    resource_type = DS8K_CS_PPRC


RESOURCE_TUPLE = (CSPPRC, CSPPRCManager)
