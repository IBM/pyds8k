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
from nose.tools import nottest
from pyds8k.resources.ds8k.v1.common import types
from ...data import get_response_list_json_by_type, \
    get_response_list_data_by_type, \
    get_response_data_by_type, \
    get_response_json_by_type
from ...data import action_response_json
from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.systems import System
from pyds8k.resources.ds8k.v1.lss import LSS
# from pyds8k.resources.ds8k.v1.ioports import IOPort
from pyds8k.resources.ds8k.v1.tserep import TSERep
from pyds8k.resources.ds8k.v1.eserep import ESERep

system_list_response = get_response_list_data_by_type(types.DS8K_SYSTEM)
system_list_response_json = get_response_list_json_by_type(types.DS8K_SYSTEM)
lss_list_response = get_response_list_data_by_type(types.DS8K_LSS)
lss_list_response_json = get_response_list_json_by_type(types.DS8K_LSS)
lss_a_response = get_response_data_by_type(types.DS8K_LSS)
lss_a_response_json = get_response_json_by_type(types.DS8K_LSS)
ioport_list_response = get_response_list_data_by_type(types.DS8K_IOPORT)
ioport_list_response_json = get_response_list_json_by_type(types.DS8K_IOPORT)
ioport_a_response = get_response_data_by_type(types.DS8K_IOPORT)
ioport_a_response_json = get_response_json_by_type(types.DS8K_IOPORT)
tserep_list_response_json = get_response_list_json_by_type(types.DS8K_TSEREP)
eserep_list_response_json = get_response_list_json_by_type(types.DS8K_ESEREP)


class TestRootResourceMixin(TestDS8KWithConnect):

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

    def test_get_lss(self):
        self._test_resource_list_by_route(types.DS8K_LSS)

    def test_get_fb_lss(self):
        self._test_get_lss_by_type(types.DS8K_VOLUME_TYPE_FB)

    def test_get_ckd_lss(self):
        self._test_get_lss_by_type(types.DS8K_VOLUME_TYPE_CKD)

    @httpretty.activate
    def _test_get_lss_by_type(self, lss_type='fb'):
        url = '/lss'
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=lss_list_response_json,
                               content_type='application/json',
                               status=200,
                               )
        self.system.get_lss(lss_type=lss_type)
        self.assertEqual([lss_type, ],
                         httpretty.last_request().querystring.get('type')
                         )

    @httpretty.activate
    def test_get_lss_by_id(self):
        lss_id = '00'
        url = '/lss/{}'.format(lss_id)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=lss_a_response_json,
                               content_type='application/json',
                               status=200,
                               )
        lss = self.system.get_lss_by_id(lss_id)
        self.assertIsInstance(lss, LSS)
        lss_data = lss_a_response['data']['lss'][0]
        self._assert_equal_between_dict_and_resource(lss_data, lss)

    def test_get_ioports(self):
        self._test_resource_list_by_route(types.DS8K_IOPORT)

    def test_get_ioport(self):
        self._test_resource_by_route(types.DS8K_IOPORT)

    def test_get_host_ports(self):
        self._test_resource_list_by_route(types.DS8K_HOST_PORT)

    def test_get_host_port(self):
        self._test_resource_by_route(types.DS8K_HOST_PORT)

    def test_get_hosts(self):
        self._test_resource_list_by_route(types.DS8K_HOST)

    def test_get_host(self):
        self._test_resource_by_route(types.DS8K_HOST)

    def test_get_pools(self):
        self._test_resource_list_by_route(types.DS8K_POOL)

    def test_get_pool(self):
        self._test_resource_by_route(types.DS8K_POOL)

    def test_get_nodes(self):
        self._test_resource_list_by_route(types.DS8K_NODE)

    def test_get_node(self):
        self._test_resource_by_route(types.DS8K_NODE)

    def test_get_marrays(self):
        self._test_resource_list_by_route(types.DS8K_MARRAY)

    def test_get_marray(self):
        self._test_resource_by_route(types.DS8K_MARRAY)

    def test_get_users(self):
        self._test_resource_list_by_route(types.DS8K_USER)

    def test_get_user(self):
        self._test_resource_by_route(types.DS8K_USER)

    def test_get_io_enclosures(self):
        self._test_resource_list_by_route(types.DS8K_IOENCLOSURE)

    def test_get_io_enclosure(self):
        self._test_resource_by_route(types.DS8K_IOENCLOSURE)

    def test_get_encryption_groups(self):
        self._test_resource_list_by_route(types.DS8K_ENCRYPTION_GROUP)

    def test_get_encryption_group(self):
        self._test_resource_by_route(types.DS8K_ENCRYPTION_GROUP)

    def test_get_flashcopies(self):
        self._test_resource_list_by_route(types.DS8K_FLASHCOPY)

    @nottest
    def test_get_flashcopy(self):
        self._test_resource_by_route(types.DS8K_FLASHCOPY)

    def test_get_pprc(self):
        self._test_resource_list_by_route(types.DS8K_PPRC)

    @nottest
    def test_get_pprc_by_id(self):
        self._test_resource_by_route(types.DS8K_PPRC)

    def test_get_events(self):
        self._test_resource_list_by_route(types.DS8K_EVENT)

    def test_get_event(self):
        self._test_resource_by_route(types.DS8K_EVENT)

    @httpretty.activate
    def test_delete_tserep_by_pool(self):
        pool_name = 'testpool_0'
        url = '/pools/{}/tserep'.format(pool_name)
        httpretty.register_uri(httpretty.DELETE,
                               self.domain + self.base_url + url,
                               body=action_response_json,
                               content_type='application/json',
                               status=204,
                               )
        self.system.delete_tserep_by_pool(pool_name)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

    @httpretty.activate
    def test_delete_eserep_by_pool(self):
        pool_name = 'testpool_0'
        url = '/pools/{}/eserep'.format(pool_name)
        httpretty.register_uri(
                               httpretty.DELETE,
                               self.domain + self.base_url + url,
                               body=action_response_json,
                               content_type='application/json',
                               status=204,
                               )
        self.system.delete_eserep_by_pool(pool_name)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

    @httpretty.activate
    def test_get_tserep_by_pool(self):
        pool_name = 'testpool_0'
        url = '/pools/{}/tserep'.format(pool_name)
        httpretty.register_uri(
                               httpretty.GET,
                               self.domain + self.base_url + url,
                               body=tserep_list_response_json,
                               content_type='application/json',
                               status=200,
                               )
        tserep = self.system.get_tserep_by_pool(pool_name)
        self.assertIsInstance(tserep, TSERep)

    @httpretty.activate
    def test_get_eserep_by_pool(self):
        pool_name = 'testpool_0'
        url = '/pools/{}/eserep'.format(pool_name)
        httpretty.register_uri(
                               httpretty.GET,
                               self.domain + self.base_url + url,
                               body=eserep_list_response_json,
                               content_type='application/json',
                               status=200,
                               )
        eserep = self.system.get_eserep_by_pool(pool_name)
        self.assertIsInstance(eserep, ESERep)

    def test_get_volumes(self):
        self._test_resource_list_by_route(types.DS8K_VOLUME)

    def test_get_volume(self):
        self._test_resource_by_route(types.DS8K_VOLUME)

    def test_get_volumes_by_lss(self):
        pass

    def test_get_volumes_by_pool(self):
        pass
