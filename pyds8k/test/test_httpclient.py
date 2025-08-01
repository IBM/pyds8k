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
import time
from functools import partial
from http import HTTPStatus

import pytest
import responses

from pyds8k.base import DefaultManager, Resource
from pyds8k.exceptions import URLParseError
from pyds8k.httpclient import HTTPClient

from . import base
from .data import (
    get_response_data_by_type,
    get_response_json_by_type,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

info = {'id': 'v1', 'name': 'vol1'}

custom_method_get = {'data': 'custom_method_get'}
custom_method_get_json = json.dumps(custom_method_get)

DEFAULT = 'default'
default_a_response = get_response_data_by_type(DEFAULT)
default_a_response_json = get_response_json_by_type(DEFAULT)
default_list_response = get_response_list_data_by_type(DEFAULT)
default_list_response_json = get_response_list_json_by_type(DEFAULT)


class TestHTTPClient(base.TestCaseWithConnect):
    def setUp(self):
        super().setUp()

    # DSANSIBLE-62, removing test_parse_url
    def test_parse_url(self):
        url1 = self.domain + '/new'
        url2 = '/new'
        _, url3 = url1.split('//')
        url4 = 'https://new_domain' + '/new'
        assert self.client._parse_url(url1) == '/new'
        assert self.client._parse_url(url2) == '/new'
        assert self.client._parse_url(url3) == '/new'
        with pytest.raises(URLParseError):
            self.client._parse_url(url4)
        new_client = HTTPClient(
            '9.115.247.115', 'admin', 'admin', service_type='ds8k', secure=True
        )
        with pytest.raises(URLParseError):
            new_client._parse_url(url3)

    @responses.activate
    def test_redirect(self):
        url = '/default/old'
        new_url = '/default/a'
        responses.get(
            self.domain + self.base_url + url,
            content_type='application/json',
            adding_headers={'Location': new_url},
            status=HTTPStatus.MOVED_PERMANENTLY,
        )
        responses.get(
            self.domain + self.base_url + new_url,
            body=default_a_response_json,
            content_type='application/json',
            status=HTTPStatus.OK,
        )
        de = self.resource.one(DEFAULT, 'old').get(allow_redirects=False)
        assert new_url == de.url

    @pytest.mark.skip(reason="Not work in this way")
    @responses.activate
    def test_timeout(self):
        url = '/default/a'
        new_client = HTTPClient(
            'localhost', 'admin', 'admin', service_type='ds8k', timeout=0.01
        )
        uri = f'{new_client.domain}{self.base_url}{url}'
        headers = {}

        def _verify_request(request, _uri=None, _headers=None):
            assert _uri == uri
            time.sleep(10)
            return (HTTPStatus.OK, _headers, default_a_response_json)

        responses.add_callback(
            responses.GET,
            uri,
            callback=partial(_verify_request, _uri=uri, _headers=headers),
            content_type='application/json',
        )
        responses.get(
            uri,
            body=_verify_request,
            content_type='application/json',
        )

        resource = Resource(new_client, DefaultManager(new_client))
        resource.one(DEFAULT, 'a').get()
