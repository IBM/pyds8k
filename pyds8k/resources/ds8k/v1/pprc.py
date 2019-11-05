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
PPRC interface.
"""

from .common.base import Base, ReadOnlyManager
from .common.types import DS8K_PPRC
from .volumes import Volume, VolumeManager
from .systems import System, SystemManager


class PPRC(Base):
    # id_field = 'id'
    _template = {'id': '',
                 'type': '',
                 'state': '',
                 'targetsystem': '',
                 'sourcevolume': '',
                 'targetvolume': '',
                 }

    related_resource = {'_sourcevolume': (Volume, VolumeManager),
                        '_targetvolume': (Volume, VolumeManager),
                        '_targetsystem': (System, SystemManager),
                        }

    def _add_details(self, info, force=False):
        super(PPRC, self)._add_details(info, force=force)

        # Temporarily, remove this line when flashcopy resource has id field.
        self._id = self.representation['id'] = '{}:{}'.format(
            info['sourcevolume']['id'],
            info['targetvolume']['id']
        )

    # def __repr__(self):
    #    return "<FlashCopy: {}>".format(self.id)


class PPRCManager(ReadOnlyManager):
    """
    Manage PPRC resources.
    """
    resource_class = PPRC
    resource_type = DS8K_PPRC


RESOURCE_TUPLE = (PPRC, PPRCManager)
