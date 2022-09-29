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

import httpretty
import json
from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_RESOURCE_GROUP
from pyds8k.test.data import get_response_json_by_type, \
    get_response_data_by_type, \
    create_resource_group_response_json, \
    action_response_json, \
    action_response

from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.resource_groups import ResourceGroup


response_a = get_response_data_by_type(DS8K_RESOURCE_GROUP)
response_a_json = get_response_json_by_type(DS8K_RESOURCE_GROUP)


class TestResourceGroup(TestDS8KWithConnect):

    def setUp(self):
        super(TestResourceGroup, self).setUp()
        self.resource_group_id = self._get_resource_id_from_resopnse(
            DS8K_RESOURCE_GROUP,
            response_a,
            ResourceGroup.id_field
            )
        self.resource_group = self.system.one(
            DS8K_RESOURCE_GROUP,
            self.resource_group_id,
            rebuild_url=True
        )

    @httpretty.activate
    def test_delete_resource_group(self):
        url = '/resource_groups/{}'.format(self.resource_group_id)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=response_a_json,
                               content_type='application/json',
                               status=200,
                               )
        httpretty.register_uri(httpretty.DELETE,
                               self.domain + self.base_url + url,
                               body=action_response_json,
                               content_type='application/json',
                               status=204,
                               )
        # Way 1
        _ = self.system.delete_resource_group(self.resource_group_id)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        resource_group = self.system.get_resource_group(self.resource_group_id)
        self.assertIsInstance(resource_group, ResourceGroup)
        resp2, _ = resource_group.delete()
        self.assertEqual(resp2.status_code, 204)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

    @httpretty.activate
    def test_update_resource_group(self):
        url = '/resource_groups/{}'.format(self.resource_group_id)
        new_name = 'new_name'
        new_label = 'new_label'
        new_cs_global = 'SECRET'
        new_pass_global = 'TOP'
        new_gm_masters = ['00', '01']
        new_gm_sessions = ['FE', 'FD']

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

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
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (200, headers, action_response_json)

        httpretty.register_uri(
                               httpretty.GET,
                               self.domain + self.base_url + url,
                               body=response_a_json,
                               content_type='application/json',
                               status=200,
                               )
        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
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
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(res, action_response['server'])

        resource_group = self.system.get_resource_group(self.resource_group_id)
        # Way 2
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp2, data2 = resource_group.update()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data2, action_response['server'])
        self.assertEqual(resp2.status_code, 200)

        # Way 3 in DS8K, save works the same as update
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp3, data3 = resource_group.save()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data3, action_response['server'])
        self.assertEqual(resp3.status_code, 200)

        # Way 4
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp4, data4 = resource_group.patch()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data4, action_response['server'])
        self.assertEqual(resp4.status_code, 200)

        # Way 5 in DS8K, put works the same as patch
        resource_group.label = new_label
        resource_group.name = new_name
        resource_group.cs_global = new_cs_global
        resource_group.pass_global = new_pass_global
        resource_group.gm_masters = new_gm_masters
        resource_group.gm_sessions = new_gm_sessions
        resp5, data5 = resource_group.put()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data5, action_response['server'])
        self.assertEqual(resp5.status_code, 200)

    @httpretty.activate
    def test_create_resource_group(self):
        url = '/resource_groups'

        label = 'group1'
        name = 'group1'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            req = RequestParser({'label': label,
                                 'name': name,
                                 }
                                )
            assert {
                    **json.loads(request.body).get('request').get('params'),
                    **req.get_request_data().get('request').get('params')
                   } == json.loads(request.body).get('request').get('params')
            return (201, headers, create_resource_group_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        # Way 1
        resp1 = self.system.create_resource_group(
            label=label,
            name=name,
        )
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(resp1[0], ResourceGroup)

        # Way 2
        resource_group = self.system.all(DS8K_RESOURCE_GROUP, rebuild_url=True)
        resource_group2 = resource_group.create(label=label, name=name, )
        resp2, data2 = resource_group2.posta()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data2[0], ResourceGroup)
        self.assertEqual(resp2.status_code, 201)

        # Way 3
        resource_group = self.system.all(DS8K_RESOURCE_GROUP, rebuild_url=True)
        resource_group3 = resource_group.create(label=label, name=name, )
        resp3, data3 = resource_group3.save()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data3[0], ResourceGroup)
        self.assertEqual(resp3.status_code, 201)

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.
