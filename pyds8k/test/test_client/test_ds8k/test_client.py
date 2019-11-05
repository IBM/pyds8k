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

from pyds8k.resources.ds8k.v1.common.types import DS8K_SYSTEM, \
    DS8K_VOLUME
from ...base import TestCaseWithConnect
from pyds8k.resources.ds8k.v1.common.base import Base
from ...data import get_response_list_json_by_type, \
    get_response_list_data_by_type
from pyds8k.client.ds8k.v1.client import Client
from pyds8k.resources.ds8k.v1.volumes import Volume
import httpretty

system_list_response_json = get_response_list_json_by_type(DS8K_SYSTEM)
volume_list_response_json = get_response_list_json_by_type(DS8K_VOLUME)
volume_list_response = get_response_list_data_by_type(DS8K_VOLUME)


class TestClient(TestCaseWithConnect):

    def setUp(self):
        super(TestClient, self).setUp()
        self.base_url = Base.base_url
        self.rest_client = Client('localhost', 'admin', 'admin', '8088')

    @httpretty.activate
    def test_get_array_method(self):
        domain = self.client.domain
        vol_url = '/volumes'
        sys_url = '/systems'
        httpretty.register_uri(httpretty.GET,
                               domain + self.base_url + vol_url,
                               body=volume_list_response_json,
                               content_type='application/json')

        httpretty.register_uri(httpretty.GET,
                               domain + self.base_url + sys_url,
                               body=system_list_response_json,
                               content_type='application/json')

        vol_list = self.rest_client.get_volumes()
        self.assertIsInstance(vol_list, list)
        self.assertIsInstance(vol_list[0], Volume)
        self.assertEqual(
                         len(vol_list),
                         len(volume_list_response['data']['volumes'])
                         )
        with self.assertRaises(AttributeError):
            # 'base_url' is an attr from System, not a method
            self.rest_client.base_url
