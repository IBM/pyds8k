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

from pyds8k.resources.ds8k.v1.common.types import DS8K_PPRC
from ...data import get_response_data_by_type
from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.resources.ds8k.v1.pprc import PPRC
from pyds8k.resources.ds8k.v1.systems import System


class TestPPRC(TestDS8KWithConnect):

    def test_related_resource_field(self):
        pprc_info = get_response_data_by_type(
            DS8K_PPRC
            )['data'][DS8K_PPRC][0]
        sourcevolume_id = pprc_info['sourcevolume'][Volume.id_field]
        targetvolume_id = pprc_info['targetvolume'][Volume.id_field]
        targetsystem_id = pprc_info['targetsystem'][System.id_field]
        pprc = PPRC(self.client, info=pprc_info)
        self.assertEqual(pprc.sourcevolume, sourcevolume_id)
        self.assertEqual(pprc.representation['sourcevolume'], sourcevolume_id)
        self.assertIsInstance(pprc._sourcevolume, Volume)
        self.assertEqual(pprc._sourcevolume.id, sourcevolume_id)
        self.assertEqual(pprc.targetvolume, targetvolume_id)
        self.assertEqual(pprc.representation['targetvolume'], targetvolume_id)
        self.assertIsInstance(pprc._targetvolume, Volume)
        self.assertEqual(pprc._targetvolume.id, targetvolume_id)
        self.assertEqual(pprc.targetsystem, targetsystem_id)
        self.assertEqual(pprc.representation['targetsystem'], targetsystem_id)
        self.assertIsInstance(pprc._targetsystem, System)
        self.assertEqual(pprc._targetsystem.id, targetsystem_id)
