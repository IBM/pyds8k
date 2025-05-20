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

import json
import warnings
from functools import cmp_to_key
from http import HTTPStatus

import httpretty
import pytest

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.exceptions import FieldReadOnly, InternalServerError
from pyds8k.messages import DEFAULT_SUCCESS_BODY_DICT
from pyds8k.resources.ds8k.v1.common.types import (
    DS8K_HOST,
    DS8K_HOST_PORT,
    DS8K_IOPORT,
    DS8K_VOLUME,
)
from pyds8k.resources.ds8k.v1.host_ports import HostPort
from pyds8k.resources.ds8k.v1.hosts import Host
from pyds8k.resources.ds8k.v1.ioports import IOPort
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.test.data import (
    action_response,
    action_response_failed,
    action_response_failed_json,
    action_response_json,
    create_host_response_json,
    get_response_data_by_type,
    get_response_json_by_type,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

from .base import TestDS8KWithConnect

volume_list_response = get_response_list_data_by_type(DS8K_VOLUME)
volume_list_response_json = get_response_list_json_by_type(DS8K_VOLUME)


class TestHost(TestDS8KWithConnect):
    def test_get_volumes(self):
        self._test_sub_resource_list_by_route(
            DS8K_HOST, DS8K_VOLUME, self._sorted_by_volume_name
        )

    def test_get_ioports(self):
        self._test_sub_resource_list_by_route(
            DS8K_HOST, DS8K_IOPORT, self._get_sort_func_by(IOPort.id_field)
        )

    def test_get_host_ports(self):
        self._test_sub_resource_list_by_route(
            DS8K_HOST, DS8K_HOST_PORT, self._get_sort_func_by(HostPort.id_field)
        )

    @httpretty.activate
    def test_delete_host(self):
        host_name = 'host1'
        url = f'/hosts/{host_name}'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=get_response_json_by_type(DS8K_HOST),
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        httpretty.register_uri(
            httpretty.DELETE,
            self.domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            status=HTTPStatus.NO_CONTENT,
        )
        # Way 1
        _ = self.system.delete_host(host_name)
        assert httpretty.last_request().method == httpretty.DELETE
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        host = self.system.get_host(host_name)
        assert isinstance(host, Host)
        resp2, _ = host.delete()
        assert resp2.status_code == HTTPStatus.NO_CONTENT
        assert httpretty.last_request().method == httpretty.DELETE
        # self.assertEqual(resp2.text, action_response['server'])
        # self.assertEqual(data2, action_response['server'])
        # warnings.warn("TestHost.test_delete_host: do not know why \

    # requests can not get DELETE response's body. Maybe httpretty can \
    # not set DELETE response's body correctly")

    @httpretty.activate
    def test_delete_host_without_resp_body(self):
        host_name = 'host1'
        url = f'/hosts/{host_name}'
        httpretty.register_uri(
            httpretty.DELETE,
            self.domain + self.base_url + url,
            content_type='application/json',
            status=HTTPStatus.NO_CONTENT,
        )
        resp1 = self.system.delete_host(host_name)
        assert httpretty.last_request().method == httpretty.DELETE
        assert resp1 == DEFAULT_SUCCESS_BODY_DICT

    @httpretty.activate
    def test_delete_host_failed(self):
        host_name = 'host1'
        url = f'/hosts/{host_name}'
        httpretty.register_uri(
            httpretty.DELETE,
            self.domain + self.base_url + url,
            body=action_response_failed_json,
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        with pytest.raises(InternalServerError) as cm:
            self.system.delete_host(host_name)
        assert action_response_failed['server'] == cm.value.error_data
        assert httpretty.last_request().method == httpretty.DELETE

    @httpretty.activate
    def test_update_host_rm_ioports_all(self):
        host_name = 'host1'
        url = f'/hosts/{host_name}'

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            resq = RequestParser({'ioports': []})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, action_response_json)

        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=get_response_json_by_type(DS8K_HOST),
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        httpretty.register_uri(
            httpretty.PUT,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        # Way 1
        resp1 = self.system.update_host_rm_ioports_all(host_name)
        assert httpretty.last_request().method == httpretty.PUT
        assert resp1 == action_response['server']

        host = self.system.get_host(host_name)
        # Way 2
        host.ioports = []
        resp2, data2 = host.update()
        assert httpretty.last_request().method == httpretty.PUT
        assert data2 == action_response['server']
        assert resp2.status_code == HTTPStatus.OK

        # Way 3 in DS8K, save works the same as update
        host.ioports = []
        resp3, data3 = host.save()
        assert httpretty.last_request().method == httpretty.PUT
        assert data3 == action_response['server']
        assert resp3.status_code == HTTPStatus.OK

        # Way 4
        host.ioports = []
        resp4, data4 = host.patch()
        assert httpretty.last_request().method == httpretty.PUT
        assert data4 == action_response['server']
        assert resp4.status_code == HTTPStatus.OK

        # Way 5 in DS8K, put works the same as patch
        host.ioports = []
        resp5, data5 = host.put()
        assert httpretty.last_request().method == httpretty.PUT
        assert data5 == action_response['server']
        assert resp5.status_code == HTTPStatus.OK

    @httpretty.activate
    def test_update_host_add_ioports_all(self):
        host_name = 'host1'
        url = f'/hosts/{host_name}'

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            resq = RequestParser({'ioports': 'all'})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, action_response_json)

        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=get_response_json_by_type(DS8K_HOST),
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        httpretty.register_uri(
            httpretty.PUT,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        # Way 1
        resp1 = self.system.update_host_add_ioports_all(host_name)
        assert httpretty.last_request().method == httpretty.PUT
        assert resp1 == action_response['server']

    @pytest.mark.skip
    @httpretty.activate
    def test_update_host_rm_volumes_all(self):
        host_name = 'host1'
        url = f'/hosts/{host_name}'

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            resq = RequestParser({'volumes': []})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, action_response_json)

        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=get_response_json_by_type(DS8K_HOST),
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        httpretty.register_uri(
            httpretty.PUT,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        # Way 1
        resp1 = self.system.update_host_rm_volumes_all(host_name)
        assert httpretty.last_request().method == httpretty.PUT
        assert resp1 == action_response['server']

        host = self.system.get_host(host_name)
        # Way 2
        host.volumes = []
        resp2, data2 = host.update()
        assert httpretty.last_request().method == httpretty.PUT
        assert data2 == action_response['server']
        assert resp2.status_code == HTTPStatus.OK

    @pytest.mark.skip
    @httpretty.activate
    def test_update_host_add_volumes(self):
        warnings.warn('test_update_host_add_volumes: not finished yet.')

    @pytest.mark.skip
    @httpretty.activate
    def test_update_host_rm_volumes(self):
        warnings.warn('test_update_host_rm_volumes: not finished yet.')

    @httpretty.activate
    def test_update_host_add_ioports(self):
        response_a_json = get_response_json_by_type(DS8K_HOST)
        response_a = get_response_data_by_type(DS8K_HOST)
        host_name = self._get_resource_id_from_resopnse(
            DS8K_HOST, response_a, Host.id_field
        )
        res_all = get_response_list_data_by_type(DS8K_IOPORT)
        ioport_ids = self._get_resource_ids_from_resopnse(
            DS8K_IOPORT, res_all, IOPort.id_field
        )
        port_id = 'new_port_id'

        url = f'/hosts/{host_name}'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK,
        )

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            ioport_ids.append(port_id)
            resq = RequestParser({'ioports': ioport_ids})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, action_response_json)

        httpretty.register_uri(
            httpretty.PUT,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        ioport_url = f'{url}/{DS8K_IOPORT}'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + ioport_url,
            body=get_response_list_json_by_type(DS8K_IOPORT),
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        host = self.system.get_host(host_name)
        resp = host.update_host_add_ioports(port_id)
        assert httpretty.last_request().method == httpretty.PUT
        assert resp == action_response['server']

    @httpretty.activate
    def test_update_host_rm_ioports(self):
        response_a_json = get_response_json_by_type(DS8K_HOST)
        response_a = get_response_data_by_type(DS8K_HOST)
        host_name = self._get_resource_id_from_resopnse(
            DS8K_HOST, response_a, Host.id_field
        )
        res_all = get_response_list_data_by_type(DS8K_IOPORT)
        ioport_ids = self._get_resource_ids_from_resopnse(
            DS8K_IOPORT, res_all, IOPort.id_field
        )
        port_id = ioport_ids[0]

        url = f'/hosts/{host_name}'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK,
        )

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            resq = RequestParser({'ioports': ioport_ids[1:]})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, action_response_json)

        httpretty.register_uri(
            httpretty.PUT,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        ioport_url = f'{url}/{DS8K_IOPORT}'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + ioport_url,
            body=get_response_list_json_by_type(DS8K_IOPORT),
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        host = self.system.get_host(host_name)
        resp = host.update_host_rm_ioports(port_id)
        assert httpretty.last_request().method == httpretty.PUT
        assert resp == action_response['server']

    @httpretty.activate
    def test_update_host_failed(self):
        host_name = 'host1'
        url = f'/hosts/{host_name}'

        httpretty.register_uri(
            httpretty.PUT,
            self.domain + self.base_url + url,
            body=action_response_failed_json,
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        with pytest.raises(InternalServerError) as cm:
            self.system.update_host_rm_ioports_all(host_name)
        assert action_response_failed['server'] == cm.value.error_data

    def test_set_readonly_field(self):
        host = Host(self.client)
        with pytest.raises(FieldReadOnly):
            host.name = 'new_name'
        with pytest.raises(FieldReadOnly):
            host.state = 'new_state'
        with pytest.raises(FieldReadOnly):
            host.addrmode = 'new_addrmode'
        with pytest.raises(FieldReadOnly):
            host.addrdiscovery = 'new_addrdiscovery'
        with pytest.raises(FieldReadOnly):
            host.lbs = 'new_lbs'

    def test_set_related_resources_collection(self):
        volumes = [Volume(self.client, resource_id=f'volume{i}') for i in range(10)]
        host_ports = [
            HostPort(self.client, resource_id=f'host_port{i}') for i in range(10)
        ]
        ioports = [IOPort(self.client, resource_id=f'ioport{i}') for i in range(10)]

        # init without related_resources collection
        host = Host(
            self.client,
            info={
                'volumes': 'volumes',  # string
                'ioports': '',  # empty
                'host_ports': {  # link
                    'link': {'rel': 'self', 'href': '/api/v1//host_ports'},
                },
            },
        )
        for i in host.related_resources_collection:
            assert host.representation.get(i) == ''
            assert not hasattr(host, i)

        # setting related resources collection
        for item in ((DS8K_VOLUME, volumes), (DS8K_IOPORT, ioports)):
            setattr(host, item[0], item[1])
            for j, value in enumerate(host.representation[item[0]]):
                assert value == getattr(item[1][j], item[1][j].id_field)
            for ind, v in enumerate(host._get_modified_info_dict()[item[0]]):
                assert v == getattr(item[1][ind], item[1][ind].id_field)

        # loading related resources collection
        host.volumes = []
        host.ioports = []
        host._start_updating()
        for item in (
            (DS8K_VOLUME, volumes),
            (DS8K_HOST_PORT, host_ports),
            (DS8K_IOPORT, ioports),
        ):
            setattr(host, item[0], item[1])
            for j, value in enumerate(host.representation[item[0]]):
                assert value == getattr(item[1][j], item[1][j].id_field)
        host._stop_updating()

    @httpretty.activate
    def test_lazy_loading_related_resources_collection(self):
        response_a_json = get_response_json_by_type(DS8K_HOST)
        response_a = get_response_data_by_type(DS8K_HOST)
        host_name = self._get_resource_id_from_resopnse(
            DS8K_HOST, response_a, Host.id_field
        )
        url = f'/hosts/{host_name}'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        for item in Host.related_resources_collection:
            sub_route_url = f'{url}/{item}'
            httpretty.register_uri(
                httpretty.GET,
                self.domain + self.base_url + sub_route_url,
                body=get_response_list_json_by_type(item),
                content_type='application/json',
                status=HTTPStatus.OK,
            )
        host = self.system.get_host(host_name)

        for item in Host.related_resources_collection:
            res_collection = getattr(host, item)
            assert len(res_collection) != 0
            res_collection.sort(
                key=cmp_to_key(self._get_sort_func_by(res_collection[0].id_field))
            )
            res_collection_data = list(
                get_response_list_data_by_type(item)['data'][item]
            )
            res_collection_data.sort(
                key=cmp_to_key(self._get_sort_func_by(res_collection[0].id_field))
            )

            assert len(res_collection_data) == len(res_collection)
            self._assert_equal_between_sorted_dict_and_resource_list(
                res_collection_data, res_collection
            )

    def test_set_related_resources_collection_during_loading(self):
        host = Host(
            self.client,
            info={
                'volumes': [
                    {
                        'id': '0000',
                        'link': {'rel': 'self', 'href': '/api/v1/volumes/0000'},
                    },
                ],
                'ioports': [
                    {
                        'id': '0030',
                        'link': {'rel': 'self', 'href': '/api/v1/ioports/0030'},
                    },
                ],  # missing
                'host_ports': [
                    {
                        'wwpn': '50050763030313A2',
                        'link': {
                            'rel': 'self',
                            'href': '/api/v1/host_ports/50050763030313A2',
                        },
                    },
                ],
            },
        )

        assert host.representation.get('volumes')[0] == '0000'
        assert host.representation.get('ioports')[0] == '0030'
        assert host.representation.get('host_ports')[0] == '50050763030313A2'
        assert host.volumes[0].id == '0000'
        assert host.ioports[0].id == '0030'
        assert host.host_ports[0].id == '50050763030313A2'

    @httpretty.activate
    def test_create_host(self):
        host_type = 'VMware'
        url = '/hosts'
        host_name = 'host1'

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            req = RequestParser({'hosttype': host_type, 'name': host_name})
            assert {
                **json.loads(request.body).get('request').get('params'),
                **req.get_request_data().get('request').get('params'),
            } == json.loads(request.body).get('request').get('params')
            return (HTTPStatus.OK, headers, create_host_response_json)

        httpretty.register_uri(
            httpretty.POST,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        # Way 1
        resp1 = self.system.create_host(host_name, host_type)
        assert httpretty.last_request().method == httpretty.POST
        assert isinstance(resp1[0], Host)

        # Way 2
        host = self.system.all(DS8K_HOST, rebuild_url=True)
        new_host2 = host.create(hosttype=host_type, name=host_name)
        resp2, data2 = new_host2.posta()
        assert httpretty.last_request().method == httpretty.POST
        assert isinstance(data2[0], Host)
        assert resp2.status_code == HTTPStatus.OK

        # Way 3
        host = self.system.all(DS8K_HOST, rebuild_url=True)
        new_host3 = host.create(hosttype=host_type, name=host_name)
        resp3, data3 = new_host3.save()
        assert httpretty.last_request().method == httpretty.POST
        assert isinstance(data3[0], Host)
        assert resp3.status_code == HTTPStatus.OK

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.

    @httpretty.activate
    def test_create_host_failed(self):
        host_type = 'VMware'
        url = '/hosts'
        host_name = 'host1'

        httpretty.register_uri(
            httpretty.POST,
            self.domain + self.base_url + url,
            body=action_response_failed_json,
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        with pytest.raises(InternalServerError) as cm:
            self.system.create_host(host_name, host_type)
        assert action_response_failed['server'] == cm.value.error_data
