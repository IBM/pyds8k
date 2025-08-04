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
from http import HTTPStatus

import httpretty
import pytest

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.exceptions import InternalServerError
from pyds8k.resources.ds8k.v1.common.types import DS8K_HOST, DS8K_VOLMAP
from pyds8k.resources.ds8k.v1.hosts import Host
from pyds8k.resources.ds8k.v1.mappings import Volmap
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.test.data import (
    action_response_failed,
    action_response_failed_json,
    action_response_json,
    create_mapping_response_json,
    create_mappings_response_json,
    get_response_data_by_type,
    get_response_json_by_type,
)

from .base import TestDS8KWithConnect

host_response = get_response_data_by_type(DS8K_HOST)
host_response_json = get_response_json_by_type(DS8K_HOST)
mapping_response = get_response_data_by_type(DS8K_VOLMAP)
mapping_response_json = get_response_json_by_type(DS8K_VOLMAP)


class TestVolmap(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()
        self.host_id = self._get_resource_id_from_resopnse(
            DS8K_HOST, host_response, Host.id_field
        )
        self.lunid = self._get_resource_id_from_resopnse(
            DS8K_VOLMAP, mapping_response, Volmap.id_field
        )
        self.host = self.system.one(
            DS8K_HOST,
            self.host_id,
            rebuild_url=True,
        )

    def test_related_resource_field(self):
        mapping_info = mapping_response['data'][DS8K_VOLMAP][0]
        volume_id = mapping_info['volume'][Volume.id_field]
        mapping = Volmap(self.client, info=mapping_info)
        assert mapping.volume == volume_id
        assert mapping.representation['volume'] == volume_id
        assert isinstance(mapping._volume, Volume)
        assert mapping._volume.id == volume_id

    def test_get_mappings(self):
        self._test_sub_resource_list_by_route(
            DS8K_HOST, DS8K_VOLMAP, self._get_sort_func_by(Volmap.id_field)
        )

    @httpretty.activate
    def test_delete_mapping(self):
        url = f'/hosts/{self.host_id}/mappings/{self.lunid}'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=mapping_response_json,
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
        _ = self.host.delete_mapping(self.lunid)
        assert httpretty.last_request().method == httpretty.DELETE
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        mapping = self.host.get_mapping(self.lunid)
        assert isinstance(mapping, Volmap)
        resp2, _ = mapping.delete()
        assert resp2.status_code == HTTPStatus.NO_CONTENT
        assert httpretty.last_request().method == httpretty.DELETE

    @httpretty.activate
    def test_delete_mapping_failed(self):
        url = f'/hosts/{self.host_id}/mappings/{self.lunid}'
        httpretty.register_uri(
            httpretty.DELETE,
            self.domain + self.base_url + url,
            body=action_response_failed_json,
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        with pytest.raises(InternalServerError) as cm:
            self.host.delete_mapping(self.lunid)
        assert action_response_failed['server'] == cm.value.error_data
        assert httpretty.last_request().method == httpretty.DELETE

    @httpretty.activate
    def test_create_mappings_with_volume_id(self):
        url = f'/hosts/{self.host_id}/mappings'
        volumes = [f'000{i}' for i in range(10)]

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            resq = RequestParser({'volumes': volumes})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, create_mappings_response_json)

        httpretty.register_uri(
            httpretty.POST,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        # Way 1
        resp1 = self.host.create_mappings(volumes=volumes)
        assert httpretty.last_request().method == httpretty.POST
        assert isinstance(resp1[0], Volmap)

    @httpretty.activate
    def test_create_mappings_with_mappings(self):
        url = f'/hosts/{self.host_id}/mappings'
        mappings = [{f'0{i}': f'000{i}'} for i in range(10)]

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            resq = RequestParser({'mappings': mappings})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, create_mappings_response_json)

        httpretty.register_uri(
            httpretty.POST,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        # Way 1
        resp1 = self.host.create_mappings(mappings=mappings)
        assert httpretty.last_request().method == httpretty.POST
        assert isinstance(resp1[0], Volmap)

    @httpretty.activate
    def test_create_mapping_with_volume_and_lunid(self):
        url = f'/hosts/{self.host_id}/mappings'
        lunid = '00'
        volume_id = '0000'

        def _verify_request(request, uri, headers):
            assert uri == f"{self.domain}{self.base_url}{url}"

            resq = RequestParser({'lunid': lunid, 'volume': volume_id})
            assert json.loads(request.body) == resq.get_request_data()
            return (HTTPStatus.OK, headers, create_mapping_response_json)

        httpretty.register_uri(
            httpretty.POST,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        mapping = self.host.all(DS8K_VOLMAP)
        new_mapping = mapping.create(lunid=lunid, volume=volume_id)
        resp, data = new_mapping.save()
        assert httpretty.last_request().method == httpretty.POST
        assert isinstance(data[0], Volmap)
        assert resp.status_code == HTTPStatus.OK

        @httpretty.activate
        def test_create_mapping_with_volume(self):
            url = f'/hosts/{self.host_id}/mappings'
            volume_id = '0000'

            def _verify_request(request, uri, headers):
                assert uri == f"{self.domain}{self.base_url}{url}"

                resq = RequestParser({'lunid': '', 'volume': volume_id})
                assert json.loads(request.body) == resq.get_request_data()
                return (HTTPStatus.OK, headers, create_mapping_response_json)

            httpretty.register_uri(
                httpretty.POST,
                self.domain + self.base_url + url,
                body=_verify_request,
                content_type='application/json',
            )
            mapping = self.host.all(DS8K_VOLMAP)
            new_mapping = mapping.create(lunid='', volume=volume_id)
            resp, data = new_mapping.save()
            assert httpretty.last_request().method == httpretty.POST
            assert isinstance(data[0], Volmap)
            assert resp.status_code == HTTPStatus.OK
