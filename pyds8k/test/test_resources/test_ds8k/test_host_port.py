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

from pyds8k.dataParser.ds8k import RequestParser

# import warnings
from pyds8k.exceptions import FieldReadOnly, InternalServerError
from pyds8k.messages import DEFAULT_SUCCESS_BODY_DICT
from pyds8k.resources.ds8k.v1.common.types import DS8K_HOST_PORT
from pyds8k.resources.ds8k.v1.host_ports import HostPort, HostPortManager
from pyds8k.resources.ds8k.v1.hosts import Host
from pyds8k.resources.ds8k.v1.ioports import IOPort
from pyds8k.test.data import (
    action_response,
    action_response_failed,
    action_response_failed_json,
    action_response_json,
    create_host_port_response_json,
    get_response_data_by_type,
    get_response_json_by_type,
)

from .base import TestDS8KWithConnect

response_a = get_response_data_by_type(DS8K_HOST_PORT)
response_a_json = get_response_json_by_type(DS8K_HOST_PORT)


class TestHostPort(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()
        self.host_port = HostPort(self.client, HostPortManager(self.client))
        self.wwpn = self._get_resource_id_from_resopnse(
            DS8K_HOST_PORT, response_a, HostPort.id_field
        )

    @responses.activate
    def test_delete_host_port(self):
        url = f'/host_ports/{self.wwpn}'
        responses.get(
            self.domain + self.base_url + url,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        responses.delete(
            self.domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        # Way 1
        _ = self.system.delete_host_port(self.wwpn)
        assert responses.calls[-1].request.method == responses.DELETE
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        host_port = self.system.get_host_port(self.wwpn)
        assert isinstance(host_port, HostPort)
        resp2, _ = host_port.delete()
        assert resp2.status_code == HTTPStatus.OK.value
        assert responses.calls[-1].request.method == responses.DELETE
        # self.assertEqual(resp2.text, action_response['server'])
        # self.assertEqual(data2, action_response['server'])
        # warnings.warn("TestHostPort.test_delete_host_port: do not know why \

    # requests can not get DELETE response's body. Maybe responses can \
    # not set DELETE response's body correctly")

    @responses.activate
    def test_delete_host_port_without_resp_body(self):
        url = f'/host_ports/{self.wwpn}'
        responses.delete(
            self.domain + self.base_url + url,
            content_type='application/json',
            status=HTTPStatus.NO_CONTENT.value,
        )
        resp1 = self.system.delete_host_port(self.wwpn)
        assert responses.calls[-1].request.method == responses.DELETE
        assert resp1 == DEFAULT_SUCCESS_BODY_DICT

    @responses.activate
    def test_delete_host_port_failed(self):
        url = f'/host_ports/{self.wwpn}'
        responses.delete(
            self.domain + self.base_url + url,
            body=action_response_failed_json,
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
        with pytest.raises(InternalServerError) as cm:
            self.system.delete_host_port(self.wwpn)
        assert action_response_failed['server'] == cm.value.error_data
        assert responses.calls[-1].request.method == responses.DELETE

    @responses.activate
    def test_update_host_port(self):
        url = f'/host_ports/{self.wwpn}'
        uri = f'{self.domain}{self.base_url}{url}'

        new_host_name = 'new_host'

        responses.get(
            uri,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        resq = RequestParser({'host': new_host_name})
        responses.put(
            uri,
            status=HTTPStatus.OK,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        # Way 1
        resp1 = self.system.update_host_port_change_host(self.wwpn, new_host_name)
        assert responses.calls[-1].request.method == responses.PUT
        assert resp1 == action_response['server']

        host_port = self.system.get_host_port(self.wwpn)

        # Way 2
        host_port.host = new_host_name
        resp2, data2 = host_port.update()
        assert responses.calls[-1].request.method == responses.PUT
        assert data2 == action_response['server']
        assert resp2.status_code == HTTPStatus.OK

        # Way 3 in DS8K, save works the same as update
        host_port.host = new_host_name
        resp3, data3 = host_port.save()
        assert responses.calls[-1].request.method == responses.PUT
        assert data3 == action_response['server']
        assert resp3.status_code == HTTPStatus.OK

        # Way 4
        host_port.host = new_host_name
        resp4, data4 = host_port.patch()
        assert responses.calls[-1].request.method == responses.PUT
        assert data4 == action_response['server']
        assert resp4.status_code == HTTPStatus.OK

        # Way 5 in DS8K, put works the same as patch
        host_port.host = new_host_name
        resp5, data5 = host_port.put()
        assert responses.calls[-1].request.method == responses.PUT
        assert data5 == action_response['server']
        assert resp5.status_code == HTTPStatus.OK

    @responses.activate
    def test_update_host_port_failed(self):
        url = f'/host_ports/{self.wwpn}'
        new_host_name = 'new_host'

        responses.put(
            self.domain + self.base_url + url,
            body=action_response_failed_json,
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
        with pytest.raises(InternalServerError) as cm:
            self.system.update_host_port_change_host(self.wwpn, new_host_name)
        assert action_response_failed['server'] == cm.value.error_data

    def test_set_readonly_field(self):
        with pytest.raises(FieldReadOnly):
            self.host_port.state = 'new_state'
        with pytest.raises(FieldReadOnly):
            self.host_port.wwpn = 'new_wwpn'

    def test_update_host_field(self):
        host_info = get_response_data_by_type(DS8K_HOST_PORT)['data'][DS8K_HOST_PORT][0]
        host_name = host_info['host']['name']
        self.host_port._add_details(host_info)
        assert self.host_port.host == host_name
        assert self.host_port.representation['host'] == host_name
        assert isinstance(self.host_port._host, Host)
        assert self.host_port._host.id == host_name

        self.host_port.host = 'new_host'
        assert self.host_port.host == 'new_host'
        assert self.host_port.representation['host'] == 'new_host'

    @responses.activate
    def test_create_host_port(self):
        url = '/host_ports'
        uri = f'{self.domain}{self.base_url}{url}'

        host_name = 'host1'

        req = RequestParser({'wwpn': self.wwpn, 'host': host_name})
        responses.post(
            uri,
            status=HTTPStatus.OK,
            body=create_host_port_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )

        # Way 1
        resp1 = self.system.create_host_port(self.wwpn, host_name)
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp1[0], HostPort)

        # Way 2
        host_port = self.system.all(DS8K_HOST_PORT, rebuild_url=True)
        new_host_port2 = host_port.create(wwpn=self.wwpn, host=host_name)
        resp2, data2 = new_host_port2.posta()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data2[0], HostPort)
        assert resp2.status_code == HTTPStatus.OK

        # Way 3
        host_port = self.system.all(DS8K_HOST_PORT, rebuild_url=True)
        new_host_port3 = host_port.create(wwpn=self.wwpn, host=host_name)
        resp3, data3 = new_host_port3.save()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data3[0], HostPort)
        assert resp3.status_code == HTTPStatus.OK

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.

    @responses.activate
    def test_create_host_port_failed(self):
        url = '/host_ports'
        host_name = 'host1'

        responses.post(
            self.domain + self.base_url + url,
            body=action_response_failed_json,
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
        with pytest.raises(InternalServerError) as cm:
            self.system.create_host_port(self.wwpn, host_name)
        assert action_response_failed['server'] == cm.value.error_data

    def test_related_resource_field(self):
        self._test_related_resource_field(DS8K_HOST_PORT)

    def test_occupied_ioports(self):
        occupied_ioports = 'login_ports'
        info = get_response_data_by_type(DS8K_HOST_PORT)['data'][DS8K_HOST_PORT][0]
        host_port = HostPort(self.client, HostPortManager(self.client), info=info)
        ioport_ids = [port.get(IOPort.id_field) for port in info[occupied_ioports]]
        # self.assertCountEqual(ioport_ids, host_port.representation.get(occupied_ioports))
        assert ioport_ids == host_port.representation.get(occupied_ioports)
        assert isinstance(getattr(host_port, occupied_ioports)[0], IOPort)
        assert getattr(host_port, occupied_ioports)[0].id in ioport_ids
