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

from pyds8k.exceptions import URLParseError
from . import base
import httpretty
import json
import time
from nose.tools import nottest
from pyds8k.httpclient import HTTPClient
from pyds8k.base import Resource, DefaultManager
from .data import get_response_list_json_by_type, \
                      get_response_list_data_by_type, \
                      get_response_data_by_type, \
                      get_response_json_by_type
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
        super(TestHTTPClient, self).setUp()
        self.base_url = ''

    def test_parse_url(self):
        url1 = self.domain + '/new'
        url2 = '/new'
        _, url3 = url1.split('//')
        url4 = 'http://new_domain' + '/new'
        self.assertEqual('/new', self.client._parse_url(url1))
        self.assertEqual('/new', self.client._parse_url(url2))
        self.assertEqual('/new', self.client._parse_url(url3))
        with self.assertRaises(URLParseError):
            self.client._parse_url(url4)
        new_client = HTTPClient('9.115.247.115', 'admin', 'admin',
                                service_type='ds8k',
                                secure=True)
        with self.assertRaises(URLParseError):
            new_client._parse_url(url3)

    @httpretty.activate
    def test_redirect(self):
        url = '/default/old'
        new_url = '/default/a'
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               content_type='application/json',
                               adding_headers={'Location': new_url},
                               status=301)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + new_url,
                               body=default_a_response_json,
                               content_type='application/json',
                               status=200)
        de = self.resource.one(DEFAULT, 'old').get(allow_redirects=False)
        self.assertEqual(new_url, de.url)

    # Not work in this way.
    @nottest
    @httpretty.activate
    def test_timeout(self):
        url = '/default/a'
        new_client = HTTPClient('localhost', 'admin', 'admin',
                                service_type='ds8k',
                                timeout=0.01)

        def _verify_request(request, uri, headers):
            time.sleep(10)
            return (200, headers, default_a_response_json)

        httpretty.register_uri(httpretty.GET,
                               new_client.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )

        resource = Resource(new_client, DefaultManager(new_client))
        resource.one(DEFAULT, 'a').get()
