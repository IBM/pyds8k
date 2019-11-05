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
import json
# import warnings
from pyds8k.exceptions import InternalServerError, FieldReadOnly
from pyds8k.messages import DEFAULT_SUCCESS_BODY_DICT
from pyds8k.resources.ds8k.v1.common.types import DS8K_HOST_PORT
from pyds8k.resources.ds8k.v1.host_ports import HostPort, \
    HostPortManager
from pyds8k.resources.ds8k.v1.ioports import IOPort
from pyds8k.resources.ds8k.v1.hosts import Host
from .base import TestDS8KWithConnect
from ...data import get_response_json_by_type, get_response_data_by_type
from ...data import action_response, action_response_json, \
    action_response_failed, action_response_failed_json, \
    create_host_port_response_json
from pyds8k.dataParser.ds8k import RequestParser

response_a = get_response_data_by_type(DS8K_HOST_PORT)
response_a_json = get_response_json_by_type(DS8K_HOST_PORT)


class TestHostPort(TestDS8KWithConnect):

    def setUp(self):
        super(TestHostPort, self).setUp()
        self.host_port = HostPort(self.client, HostPortManager(self.client))
        self.wwpn = self._get_resource_id_from_resopnse(DS8K_HOST_PORT,
                                                        response_a,
                                                        HostPort.id_field
                                                        )

    @httpretty.activate
    def test_delete_host_port(self):
        url = '/host_ports/{}'.format(self.wwpn)
        httpretty.register_uri(
                               httpretty.GET,
                               self.domain + self.base_url + url,
                               body=response_a_json,
                               content_type='application/json',
                               status=200,
                               )
        httpretty.register_uri(
                               httpretty.DELETE,
                               self.domain + self.base_url + url,
                               body=action_response_json,
                               content_type='application/json',
                               status=204,
                               )
        # Way 1
        _ = self.system.delete_host_port(self.wwpn)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        host_port = self.system.get_host_port(self.wwpn)
        self.assertIsInstance(host_port, HostPort)
        resp2, _ = host_port.delete()
        self.assertEqual(resp2.status_code, 204)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)
        # self.assertEqual(resp2.text, action_response['server'])
        # self.assertEqual(data2, action_response['server'])
        # warnings.warn("TestHostPort.test_delete_host_port: do not know why \
# requests can not get DELETE response's body. Maybe httpretty can \
# not set DELETE response's body correctly")

    @httpretty.activate
    def test_delete_host_port_without_resp_body(self):
        url = '/host_ports/{}'.format(self.wwpn)
        httpretty.register_uri(httpretty.DELETE,
                               self.domain + self.base_url + url,
                               content_type='application/json',
                               status=204,
                               )
        resp1 = self.system.delete_host_port(self.wwpn)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)
        self.assertEqual(resp1, DEFAULT_SUCCESS_BODY_DICT)

    @httpretty.activate
    def test_delete_host_port_failed(self):
        url = '/host_ports/{}'.format(self.wwpn)
        httpretty.register_uri(
                               httpretty.DELETE,
                               self.domain + self.base_url + url,
                               body=action_response_failed_json,
                               content_type='application/json',
                               status=500,
                               )
        with self.assertRaises(InternalServerError) as cm:
            self.system.delete_host_port(self.wwpn)
        self.assertEqual(action_response_failed['server'],
                         cm.exception.error_data
                         )
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

    @httpretty.activate
    def test_update_host_port(self):
        url = '/host_ports/{}'.format(self.wwpn)
        new_host_name = 'new_host'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'host': new_host_name})
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
        resp1 = self.system.update_host_port_change_host(self.wwpn,
                                                         new_host_name
                                                         )
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(resp1, action_response['server'])

        host_port = self.system.get_host_port(self.wwpn)

        # Way 2
        host_port.host = new_host_name
        resp2, data2 = host_port.update()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data2, action_response['server'])
        self.assertEqual(resp2.status_code, 200)

        # Way 3 in DS8K, save works the same as update
        host_port.host = new_host_name
        resp3, data3 = host_port.save()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data3, action_response['server'])
        self.assertEqual(resp3.status_code, 200)

        # Way 4
        host_port.host = new_host_name
        resp4, data4 = host_port.patch()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data4, action_response['server'])
        self.assertEqual(resp4.status_code, 200)

        # Way 5 in DS8K, put works the same as patch
        host_port.host = new_host_name
        resp5, data5 = host_port.put()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(data5, action_response['server'])
        self.assertEqual(resp5.status_code, 200)

    @httpretty.activate
    def test_update_host_port_failed(self):
        url = '/host_ports/{}'.format(self.wwpn)
        new_host_name = 'new_host'

        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=action_response_failed_json,
                               content_type='application/json',
                               status=500
                               )
        with self.assertRaises(InternalServerError) as cm:
            self.system.update_host_port_change_host(self.wwpn, new_host_name)
        self.assertEqual(action_response_failed['server'],
                         cm.exception.error_data
                         )

    def test_set_readonly_field(self):
        with self.assertRaises(FieldReadOnly):
            self.host_port.state = 'new_state'
        with self.assertRaises(FieldReadOnly):
            self.host_port.wwpn = 'new_wwpn'

    def test_update_host_field(self):
        host_info = get_response_data_by_type(
                                              DS8K_HOST_PORT
                                              )['data'][DS8K_HOST_PORT][0]
        host_name = host_info['host']['name']
        self.host_port._add_details(host_info)
        self.assertEqual(
                         self.host_port.host,
                         host_name
                         )
        self.assertEqual(
                         self.host_port.representation['host'],
                         host_name
                         )
        self.assertIsInstance(self.host_port._host, Host)
        self.assertEqual(
                         self.host_port._host.id,
                         host_name
                         )

        self.host_port.host = 'new_host'
        self.assertEqual(
                         self.host_port.host,
                         'new_host'
                         )
        self.assertEqual(
                         self.host_port.representation['host'],
                         'new_host'
                         )

    @httpretty.activate
    def test_create_host_port(self):
        url = '/host_ports'
        host_name = 'host1'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            req = RequestParser({'wwpn': self.wwpn, 'host': host_name})
            self.assertDictContainsSubset(
                req.get_request_data().get('request').get('params'),
                json.loads(request.body).get('request').get('params'),
            )
            return (200, headers, create_host_port_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        # Way 1
        resp1 = self.system.create_host_port(self.wwpn, host_name)
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(resp1[0], HostPort)

        # Way 2
        host_port = self.system.all(DS8K_HOST_PORT, rebuild_url=True)
        new_host_port2 = host_port.create(wwpn=self.wwpn, host=host_name)
        resp2, data2 = new_host_port2.posta()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data2[0], HostPort)
        self.assertEqual(resp2.status_code, 200)

        # Way 3
        host_port = self.system.all(DS8K_HOST_PORT, rebuild_url=True)
        new_host_port3 = host_port.create(wwpn=self.wwpn, host=host_name)
        resp3, data3 = new_host_port3.save()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data3[0], HostPort)
        self.assertEqual(resp3.status_code, 200)

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.

    @httpretty.activate
    def test_create_host_port_failed(self):
        url = '/host_ports'
        host_name = 'host1'

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=action_response_failed_json,
                               content_type='application/json',
                               status=500
                               )
        with self.assertRaises(InternalServerError) as cm:
            self.system.create_host_port(self.wwpn, host_name)
        self.assertEqual(action_response_failed['server'],
                         cm.exception.error_data
                         )

    def test_related_resource_field(self):
        self._test_related_resource_field(DS8K_HOST_PORT)

    def test_occupied_ioports(self):
        OCCUPIED_IOPORTS = 'login_ports'
        info = get_response_data_by_type(
            DS8K_HOST_PORT
            )['data'][DS8K_HOST_PORT][0]
        host_port = HostPort(self.client,
                             HostPortManager(self.client),
                             info=info
                             )
        ioport_ids = [port.get(IOPort.id_field)
                      for port in info[OCCUPIED_IOPORTS]
                      ]
        self.assertCountEqual(ioport_ids,
                              host_port.representation.get(OCCUPIED_IOPORTS)
                              )
        self.assertIsInstance(getattr(host_port, OCCUPIED_IOPORTS)[0], IOPort)
        self.assertIn(getattr(host_port, OCCUPIED_IOPORTS)[0].id, ioport_ids)
