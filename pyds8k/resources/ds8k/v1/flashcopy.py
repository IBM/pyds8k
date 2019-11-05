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
FlashCopy interface.
"""

from .common.base import Base, ReadOnlyManager
from .common.types import DS8K_FLASHCOPY
from .volumes import Volume, VolumeManager


class FlashCopy(Base):
    # id_field = 'id'
    _template = {'id': '',
                 'persistent': '',
                 'recording': '',
                 'backgroundcopy': '',
                 'state': '',
                 'sourcevolume': '',
                 'targetvolume': '',
                 }

    related_resource = {'_sourcevolume': (Volume, VolumeManager),
                        '_targetvolume': (Volume, VolumeManager)
                        }

    def _add_details(self, info, force=False):
        super(FlashCopy, self)._add_details(info, force=force)

        # Temporarily, remove this line when flashcopy resource has id field.
        self._id = self.representation['id'] = '{}:{}'.format(
            info['sourcevolume']['id'],
            info['targetvolume']['id']
        )

    # def __repr__(self):
    #    return "<FlashCopy: {}>".format(self.id)


class FlashCopyManager(ReadOnlyManager):
    """
    Manage FlashCopy resources.
    """
    resource_class = FlashCopy
    resource_type = DS8K_FLASHCOPY


RESOURCE_TUPLE = (FlashCopy, FlashCopyManager)
