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
import six
from pyds8k.base import ManagerMeta, ResourceMeta
from ..common.base import Base, ReadOnlyManager
from ..common.types import DS8K_CS_PPRC
from ..volumes import Volume, VolumeManager
from ..systems import System, SystemManager


@six.add_metaclass(ResourceMeta)
class PPRC(Base):
    resource_type = DS8K_CS_PPRC

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

    def _update_volume_info(self, info):
        # Handle for bug in DS8000 RESTful API /api/v1/cs/pprcs:
        # When it responds, source_volume and target_volume use
        # "name" as the key of id field.
        for key in ['source_volume', 'target_volume']:
            if 'name' in info[key] and 'id' not in info[key]:
                info[key]['id'] = info[key].pop('name')
        return info

    def _add_details(self, info, force=False):
        self._start_updating()
        self._update_volume_info(info)
        self._stop_updating()
        super(PPRC, self)._add_details(info, force=force)


@six.add_metaclass(ManagerMeta)
class PPRCManager(ReadOnlyManager):
    """
    Manage advanced PPRC resources.
    """
    resource_class = PPRC
    resource_type = DS8K_CS_PPRC
