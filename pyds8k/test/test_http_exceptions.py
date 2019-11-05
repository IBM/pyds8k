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
from . import base
from pyds8k import exceptions
from .data import get_response_data_by_type
from pyds8k.resources.ds8k.v1.common.base import Base

default_a_response = get_response_data_by_type('default')
response_401 = {
  "server": {
    "status": "failed",
    "code": "BE742607",
    "message": "The token is invalid or expired."
  }
}

response_token = {
  "server": {
    "status": "ok",
    "code": "",
    "message": "Operation done successfully."
  },
  "token": {
    "token": "54546d2a",
    "expired_time": "2014-08-29T20:13:24+0800",
    "max_idle_interval": "1800000"
  }
}

response_token_error = {
  "server": {
    "status": "failed",
    "code": "NIServerException",
    "message": "Operation done successfully."
  }
}

DEFAULT = 'default'


class TestHTTPException(base.TestCaseWithConnect):

    def setUp(self):
        super(TestHTTPException, self).setUp()
        self.base_url = ''

    @httpretty.activate
    def test_response_status_400(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=400
        )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.BadRequest, vol.get)

    @httpretty.activate
    def test_response_status_401(self):
        domain = self.client.domain
        url = '/default/a'
        _base_url = Base.base_url
        httpretty.register_uri(
            httpretty.POST,
            domain + _base_url + '/tokens',
            body=json.dumps(response_token),
            content_type='application/json',
            status=200
        )

        httpretty.register_uri(
            httpretty.GET,
            domain + self.base_url + url,
            responses=[
                httpretty.Response(body=json.dumps(response_401),
                                   content_type='application/json',
                                   status=401
                                   ),
                httpretty.Response(body=json.dumps(default_a_response),
                                   content_type='application/json',
                                   status=200
                                   ),
                httpretty.Response(body=json.dumps(response_401),
                                   content_type='application/json',
                                   status=401
                                   ),
            ]
        )
        vol = self.resource.one(DEFAULT, 'a')
        vol.get()
        self.assertEqual(
                    vol.url,
                    default_a_response['data']['default'][0]['link']['href']
                         )
        self.assertEqual(
                         vol.name,
                         default_a_response['data']['default'][0]['name']
                         )
        self.assertRaises(exceptions.Unauthorized, vol.get)

    @httpretty.activate
    def test_auth_fail(self):
        domain = self.client.domain
        url = '/default/a'
        _base_url = Base.base_url
        httpretty.register_uri(httpretty.POST,
                               domain + _base_url + '/tokens',
                               body=json.dumps(response_token_error),
                               content_type='application/json',
                               status=401)

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            responses=[
                httpretty.Response(body=json.dumps(response_401),
                                   content_type='application/json',
                                   status=401
                                   ),
                httpretty.Response(body=json.dumps(default_a_response),
                                   content_type='application/json',
                                   status=200
                                   ),
                httpretty.Response(body=json.dumps(response_401),
                                   content_type='application/json',
                                   status=401
                                   ),
            ]
        )
        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.Unauthorized, vol.get)

    @httpretty.activate
    def test_response_status_403(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET,
            domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=403
            )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.Forbidden, vol.get)

    @httpretty.activate
    def test_response_status_404(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=404
        )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.NotFound, vol.get)

    @httpretty.activate
    def test_response_status_405(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=405
            )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.MethodNotAllowed, vol.get)

    @httpretty.activate
    def test_response_status_409(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=409
            )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.Conflict, vol.get)

    @httpretty.activate
    def test_response_status_415(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=415
            )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.UnsupportedMediaType, vol.get)

    @httpretty.activate
    def test_response_status_500(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=500
        )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.InternalServerError, vol.get)

    @httpretty.activate
    def test_response_status_503(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=503
            )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.ServiceUnavailable, vol.get)

    @httpretty.activate
    def test_response_status_504(self):
        domain = self.client.domain
        url = '/default/a'

        httpretty.register_uri(
            httpretty.GET, domain + self.base_url + url,
            body=json.dumps(
                {'server': {'message': 'error', 'details': 'error'}}
            ),
            content_type='application/json',
            status=504
            )

        vol = self.resource.one(DEFAULT, 'a')
        self.assertRaises(exceptions.GatewayTimeout, vol.get)
