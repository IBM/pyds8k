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

import httpretty
from pyds8k.resources.ds8k.v1.common.types import DS8K_SYSTEM
from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.systems import System, \
    SystemManager
from ...data import get_response_list_json_by_type, \
    get_response_list_data_by_type
from pyds8k.exceptions import OperationNotAllowed

system_list_response = get_response_list_data_by_type(DS8K_SYSTEM)
system_list_response_json = get_response_list_json_by_type(DS8K_SYSTEM)


class TestSystem(TestDS8KWithConnect):

    def setUp(self):
        super(TestSystem, self).setUp()
        self.system = System(self.client, SystemManager(self.client))

    @httpretty.activate
    def test_get_system(self):
        url = '/systems'
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=system_list_response_json,
                               content_type='application/json',
                               status=200,
                               )
        sys = self.system.get_system()
        self.assertIsInstance(sys, System)
        sys_data = system_list_response['data']['systems'][0]
        self._assert_equal_between_dict_and_resource(sys_data, sys)

    @httpretty.activate
    def test_not_allowed_operations(self):
        url = '/systems'
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=system_list_response_json,
                               content_type='application/json',
                               status=200,
                               )
        sys = self.system.get_system()
        with self.assertRaises(OperationNotAllowed):
            sys.put()
        with self.assertRaises(OperationNotAllowed):
            sys.patch()
        with self.assertRaises(OperationNotAllowed):
            sys.posta()
        with self.assertRaises(OperationNotAllowed):
            sys.delete()
        with self.assertRaises(OperationNotAllowed):
            sys.update()
        with self.assertRaises(OperationNotAllowed) as cm:
            sys.save()
        self.assertEqual(System.__name__, cm.exception.resource_name)
