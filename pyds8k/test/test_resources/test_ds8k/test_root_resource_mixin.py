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

from http import HTTPStatus

import pytest
import responses
from responses import matchers

from pyds8k.resources.ds8k.v1.common import types
from pyds8k.resources.ds8k.v1.eserep import ESERep
from pyds8k.resources.ds8k.v1.lss import LSS
from pyds8k.resources.ds8k.v1.systems import System

# from pyds8k.resources.ds8k.v1.ioports import IOPort
from pyds8k.resources.ds8k.v1.tserep import TSERep
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.test.data import (
    action_response_json,
    get_response_data_by_type,
    get_response_json_by_type,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

from .base import TestDS8KWithConnect

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
volume_list_response = get_response_list_data_by_type(types.DS8K_VOLUME)
volume_list_response_json = get_response_list_json_by_type(types.DS8K_VOLUME)
resource_group_list_response = get_response_list_data_by_type(types.DS8K_RESOURCE_GROUP)
resource_group_list_response_json = get_response_list_json_by_type(
    types.DS8K_RESOURCE_GROUP
)


class TestRootResourceMixin(TestDS8KWithConnect):
    @responses.activate
    def test_get_system(self):
        url = '/systems'
        responses.get(
            self.domain + self.base_url + url,
            body=system_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        sys = self.system.get_system()
        assert isinstance(sys, System)
        sys_data = system_list_response['data']['systems'][0]
        self._assert_equal_between_dict_and_resource(sys_data, sys)

    def test_get_lss(self):
        self._test_resource_list_by_route(types.DS8K_LSS)

    def test_get_fb_lss(self):
        self._test_get_lss_by_type(types.DS8K_VOLUME_TYPE_FB)

    def test_get_ckd_lss(self):
        self._test_get_lss_by_type(types.DS8K_VOLUME_TYPE_CKD)

    @responses.activate
    def _test_get_lss_by_type(self, lss_type='fb'):
        url = '/lss'
        params = {'type': lss_type}

        responses.get(
            self.domain + self.base_url + url,
            body=lss_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
            match=[matchers.query_param_matcher(params)],
        )
        self.system.get_lss(lss_type=lss_type)

    @responses.activate
    def test_get_lss_by_id(self):
        lss_id = '00'
        url = f'/lss/{lss_id}'
        responses.get(
            self.domain + self.base_url + url,
            body=lss_a_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        lss = self.system.get_lss_by_id(lss_id)
        assert isinstance(lss, LSS)
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

    @pytest.mark.skip
    def test_get_flashcopy(self):
        self._test_resource_by_route(types.DS8K_FLASHCOPY)

    def test_get_pprc(self):
        self._test_resource_list_by_route(types.DS8K_PPRC)

    @pytest.mark.skip
    def test_get_pprc_by_id(self):
        self._test_resource_by_route(types.DS8K_PPRC)

    def test_get_events(self):
        self._test_resource_list_by_route(types.DS8K_EVENT)

    def test_get_event(self):
        self._test_resource_by_route(types.DS8K_EVENT)

    @responses.activate
    def test_delete_tserep_by_pool(self):
        pool_name = 'testpool_0'
        url = f'/pools/{pool_name}/tserep'
        responses.delete(
            self.domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        self.system.delete_tserep_by_pool(pool_name)
        assert responses.calls[-1].request.method == responses.DELETE

    @responses.activate
    def test_delete_eserep_by_pool(self):
        pool_name = 'testpool_0'
        url = f'/pools/{pool_name}/eserep'
        responses.delete(
            self.domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        self.system.delete_eserep_by_pool(pool_name)
        assert responses.calls[-1].request.method == responses.DELETE

    @responses.activate
    def test_get_tserep_by_pool(self):
        pool_name = 'testpool_0'
        url = f'/pools/{pool_name}/tserep'
        responses.get(
            self.domain + self.base_url + url,
            body=tserep_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        tserep = self.system.get_tserep_by_pool(pool_name)
        assert isinstance(tserep, TSERep)

    @responses.activate
    def test_get_eserep_by_pool(self):
        pool_name = 'testpool_0'
        url = f'/pools/{pool_name}/eserep'
        responses.get(
            self.domain + self.base_url + url,
            body=eserep_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        eserep = self.system.get_eserep_by_pool(pool_name)
        assert isinstance(eserep, ESERep)

    def test_get_volumes(self):
        self._test_resource_list_by_route(types.DS8K_VOLUME)

    def test_get_volume(self):
        self._test_resource_by_route(types.DS8K_VOLUME)

    @responses.activate
    def test_get_volumes_by_host(self):
        host_name = 'testhost'
        url = f'/hosts/{host_name}/volumes'
        responses.get(
            self.domain + self.base_url + url,
            body=volume_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        vol_list = self.system.get_volumes_by_host(host_name=host_name)
        assert isinstance(vol_list, list)
        assert isinstance(vol_list[0], Volume)
        assert len(vol_list) == len(volume_list_response['data']['volumes'])

    @responses.activate
    def test_get_volumes_by_lss(self):
        lss_id = '00'
        url = f'/lss/{lss_id}/volumes'
        responses.get(
            self.domain + self.base_url + url,
            body=volume_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        vol_list = self.system.get_volumes_by_lss(lss_id=lss_id)
        assert isinstance(vol_list, list)
        assert isinstance(vol_list[0], Volume)
        assert len(vol_list) == len(volume_list_response['data']['volumes'])

    @responses.activate
    def test_get_volumes_by_pool(self):
        pool_id = 'P0'
        url = f'/pools/{pool_id}/volumes'
        responses.get(
            self.domain + self.base_url + url,
            body=volume_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        vol_list = self.system.get_volumes_by_pool(pool_id=pool_id)
        assert isinstance(vol_list, list)
        assert isinstance(vol_list[0], Volume)
        assert len(vol_list) == len(volume_list_response['data']['volumes'])

    def test_get_resource_groups(self):
        self._test_resource_list_by_route(types.DS8K_RESOURCE_GROUP)

    def test_get_resource_group(self):
        self._test_resource_by_route(types.DS8K_RESOURCE_GROUP)
