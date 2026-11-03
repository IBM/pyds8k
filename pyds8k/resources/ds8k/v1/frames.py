##############################################################################
# Copyright 2026 IBM Corp.
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
Frame Enclosure interface.
"""

from .common.base import Base, ReadOnlyManager
from .common.types import DS8K_FRAME


class Frame(Base):
    resource_type = DS8K_FRAME
    alias = {
        'ID': 'id',
        'frm#': 'frm_num',  # frm# isn't a valid python identifier/attribute name
    }
    _template = {
        'frm_num': '',
        'Frame': '',
        'loc': '',
    }

    def _add_id_to_url(self, resource_id):
        # The API has no per-frame endpoint, so keep the collection url.
        pass


class FrameManager(ReadOnlyManager):
    """
    Manage Frame Enclosure resources.
    """

    resource_class = Frame
    resource_type = DS8K_FRAME
