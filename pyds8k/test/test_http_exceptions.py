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

import pytest
import responses

from pyds8k import exceptions

from . import base
from .data import get_response_data_by_type

default_a_response = get_response_data_by_type('default')
response_401 = {
    "server": {
        "status": "failed",
        "code": "BE742607",
        "message": "The token is invalid or expired.",
    }
}

response_token = {
    "server": {"status": "ok", "code": "", "message": "Operation done successfully."},
    "token": {
        "token": "54546d2a",
        "expired_time": "2014-08-29T20:13:24+0800",
        "max_idle_interval": "1800000",
    },
}

response_token_error = {
    "server": {
        "status": "failed",
        "code": "NIServerException",
        "message": "Operation done successfully.",
    }
}

DEFAULT = 'default'


class TestHTTPException(base.TestCaseWithConnect):
    def setUp(self):
        super().setUp()

    @responses.activate
    def test_response_status_400(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.BAD_REQUEST.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.BadRequest):
            vol.get()

    @responses.activate
    def test_response_status_401(self):
        domain = self.client.domain
        url = '/default/a'
        uri_base = f'{domain}{self.base_url}'
        uri = f'{uri_base}{url}'

        responses.post(
            f'{uri_base}/tokens',
            body=json.dumps(response_token),
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        responses.get(
            uri,
            body=json.dumps(response_401),
            content_type='application/json',
            status=HTTPStatus.UNAUTHORIZED.value,
        )
        responses.get(
            uri,
            body=json.dumps(default_a_response),
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        responses.get(
            uri,
            body=json.dumps(response_401),
            content_type='application/json',
            status=HTTPStatus.UNAUTHORIZED.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        vol.get()
        assert vol.url == default_a_response['data']['default'][0]['link']['href']
        assert vol.name == default_a_response['data']['default'][0]['name']
        with pytest.raises(exceptions.Unauthorized):
            vol.get()

    @responses.activate
    def test_auth_fail(self):
        domain = self.client.domain
        url = '/default/a'
        uri_base = f'{domain}{self.base_url}'
        uri = f'{uri_base}{url}'

        responses.post(
            f'{uri_base}/tokens',
            body=json.dumps(response_token_error),
            content_type='application/json',
            status=HTTPStatus.UNAUTHORIZED.value,
        )

        responses.get(
            uri,
            body=json.dumps(response_401),
            content_type='application/json',
            status=HTTPStatus.UNAUTHORIZED.value,
        )
        responses.get(
            uri,
            body=json.dumps(default_a_response),
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        responses.get(
            uri,
            body=json.dumps(response_401),
            content_type='application/json',
            status=HTTPStatus.UNAUTHORIZED.value,
        )
        responses.get(uri)
        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.Unauthorized):
            vol.get()

    @responses.activate
    def test_response_status_403(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.FORBIDDEN.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.Forbidden):
            vol.get()

    @responses.activate
    def test_response_status_404(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.NOT_FOUND.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.NotFound):
            vol.get()

    @responses.activate
    def test_response_status_405(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.METHOD_NOT_ALLOWED.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.MethodNotAllowed):
            vol.get()

    @responses.activate
    def test_response_status_409(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.CONFLICT.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.Conflict):
            vol.get()

    @responses.activate
    def test_response_status_415(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.UnsupportedMediaType):
            vol.get()

    @responses.activate
    def test_response_status_500(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.InternalServerError):
            vol.get()

    @responses.activate
    def test_response_status_503(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.SERVICE_UNAVAILABLE.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.ServiceUnavailable):
            vol.get()

    @responses.activate
    def test_response_status_504(self):
        domain = self.client.domain
        url = '/default/a'
        uri = f'{domain}{self.base_url}{url}'

        responses.get(
            uri,
            body=json.dumps({'server': {'message': 'error', 'details': 'error'}}),
            content_type='application/json',
            status=HTTPStatus.GATEWAY_TIMEOUT.value,
        )

        vol = self.resource.one(DEFAULT, 'a')
        with pytest.raises(exceptions.GatewayTimeout):
            vol.get()
