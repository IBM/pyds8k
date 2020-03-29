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

from pyds8k.resources.ds8k.v1.common.types import DS8K_CS_PPRC
from pyds8k.test.data import get_response_data_by_type
from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.resources.ds8k.v1.cs.pprcs import PPRC
from pyds8k.resources.ds8k.v1.systems import System


class TestPPRC(TestDS8KWithConnect):

    def test_related_resource_field(self):
        pprc_info = get_response_data_by_type(
            DS8K_CS_PPRC
            )['data'][DS8K_CS_PPRC][0]
        sourcevolume_id = pprc_info['source_volume'][Volume.id_field]
        targetvolume_id = pprc_info['target_volume'][Volume.id_field]
        targetsystem_id = pprc_info['target_system'][System.id_field]
        sourcesystem_id = pprc_info['source_system'][System.id_field]
        pprc = PPRC(self.client, info=pprc_info)
        self.assertEqual(pprc.source_volume, sourcevolume_id)
        self.assertEqual(pprc.representation['source_volume'], sourcevolume_id)
        self.assertIsInstance(pprc._source_volume, Volume)
        self.assertEqual(pprc._source_volume.id, sourcevolume_id)
        self.assertEqual(pprc.target_volume, targetvolume_id)
        self.assertEqual(pprc.representation['target_volume'], targetvolume_id)
        self.assertIsInstance(pprc._target_volume, Volume)
        self.assertEqual(pprc._target_volume.id, targetvolume_id)
        self.assertEqual(pprc.target_system, targetsystem_id)
        self.assertEqual(pprc.representation['target_system'], targetsystem_id)
        self.assertIsInstance(pprc._target_system, System)
        self.assertEqual(pprc._target_system.id, targetsystem_id)
        self.assertEqual(pprc.representation['source_system'], sourcesystem_id)
        self.assertIsInstance(pprc._target_system, System)
        self.assertEqual(pprc._target_system.id, targetsystem_id)
