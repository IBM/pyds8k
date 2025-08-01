##############################################################################
# Copyright 2022 IBM Corp.
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

import responses
from responses import matchers

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_RESOURCE_GROUP
from pyds8k.resources.ds8k.v1.resource_groups import ResourceGroup
from pyds8k.test.data import (
    action_response,
    action_response_json,
    create_resource_group_response_json,
    get_response_data_by_type,
    get_response_json_by_type,
)

from .base import TestDS8KWithConnect

response_a = get_response_data_by_type(DS8K_RESOURCE_GROUP)
response_a_json = get_response_json_by_type(DS8K_RESOURCE_GROUP)


class TestResourceGroup(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()
        self.resource_group_id = self._get_resource_id_from_resopnse(
            DS8K_RESOURCE_GROUP, response_a, ResourceGroup.id_field
        )
        self.resource_group = self.system.one(
            DS8K_RESOURCE_GROUP, self.resource_group_id, rebuild_url=True
        )

    @responses.activate
    def test_delete_resource_group(self):
        url = f'/resource_groups/{self.resource_group_id}'
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
        _ = self.system.delete_resource_group(self.resource_group_id)
        assert responses.calls[-1].request.method == responses.DELETE
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        resource_group = self.system.get_resource_group(self.resource_group_id)
        assert isinstance(resource_group, ResourceGroup)
        resp2, _ = resource_group.delete()
        assert resp2.status_code == HTTPStatus.OK
        assert responses.calls[-1].request.method == responses.DELETE

    @responses.activate
    def test_update_resource_group(self):
        url = f'/resource_groups/{self.resource_group_id}'
        uri = f'{self.domain}{self.base_url}{url}'

        new_name = 'new_name'
        new_label = 'new_label'
        new_cs_global = 'SECRET'
        new_pass_global = 'TOP'
        new_gm_masters = ['00', '01']
        new_gm_sessions = ['FE', 'FD']

        responses.get(
            uri,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        resq = RequestParser(
            {
                'name': new_name,
                'label': new_label,
                'cs_global': new_cs_global,
                'pass_global': new_pass_global,
                'gm_masters': new_gm_masters,
                'gm_sessions': new_gm_sessions,
            },
        )
        responses.put(
            uri,
            status=HTTPStatus.OK.value,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        # Way 1
        res = self.system.update_resource_group(
            self.resource_group_id,
            label=new_label,
            name=new_name,
            cs_global=new_cs_global,
            pass_global=new_pass_global,
            gm_masters=new_gm_masters,
            gm_sessions=new_gm_sessions,
        )
        assert responses.calls[-1].request.method == responses.PUT
        assert res == action_response['server']

        resource_group = self.system.get_resource_group(self.resource_group_id)
        # Way 2
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp2, data2 = resource_group.update()
        assert responses.calls[-1].request.method == responses.PUT
        assert data2 == action_response['server']
        assert resp2.status_code == HTTPStatus.OK

        # Way 3 in DS8K, save works the same as update
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp3, data3 = resource_group.save()
        assert responses.calls[-1].request.method == responses.PUT
        assert data3 == action_response['server']
        assert resp3.status_code == HTTPStatus.OK

        # Way 4
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp4, data4 = resource_group.patch()
        assert responses.calls[-1].request.method == responses.PUT
        assert data4 == action_response['server']
        assert resp4.status_code == HTTPStatus.OK

        # Way 5 in DS8K, put works the same as patch
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp5, data5 = resource_group.put()
        assert responses.calls[-1].request.method == responses.PUT
        assert data5 == action_response['server']
        assert resp5.status_code == HTTPStatus.OK

    @responses.activate
    def test_create_resource_group(self):
        url = '/resource_groups'
        uri = f'{self.domain}{self.base_url}{url}'

        label = 'group1'
        name = 'group1'

        req = RequestParser(
            {
                'label': label,
                'name': name,
            }
        )
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=create_resource_group_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )

        # Way 1
        resp1 = self.system.create_resource_group(
            label=label,
            name=name,
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp1[0], ResourceGroup)

        # Way 2
        resource_group = self.system.all(DS8K_RESOURCE_GROUP, rebuild_url=True)
        resource_group2 = resource_group.create(
            label=label,
            name=name,
        )
        resp2, data2 = resource_group2.posta()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data2[0], ResourceGroup)
        assert resp2.status_code == HTTPStatus.CREATED

        # Way 3
        resource_group = self.system.all(DS8K_RESOURCE_GROUP, rebuild_url=True)
        resource_group3 = resource_group.create(
            label=label,
            name=name,
        )
        resp3, data3 = resource_group3.save()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data3[0], ResourceGroup)
        assert resp3.status_code == HTTPStatus.CREATED

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.
