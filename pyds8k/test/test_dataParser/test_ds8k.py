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

from pyds8k.dataParser.ds8k import RequestParser, ResponseParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_VOLUME
from pyds8k.test import base
from pyds8k.test.data import (
    default_request,
    get_response_data_by_type,
    get_response_list_data_by_type,
    token_response_error,
)

info = {'id': 'v1', 'name': 'vol1'}

custom_method_get = {'data': 'custom_method_get'}
custom_method_post = {'data': 'custom_method_post'}
custom_method_get_json = json.dumps(custom_method_get)
custom_method_post_json = json.dumps(custom_method_post)
volume_a_response = get_response_data_by_type(DS8K_VOLUME)
volume_list_response = get_response_list_data_by_type(DS8K_VOLUME)


class TestDataParser(base.TestCaseWithoutConnect):
    def test_responseParser(self):  # noqa: N802
        re = ResponseParser(volume_a_response, 'volumes')
        assert re.response_key == 'data'
        assert re.url_field == 'link'
        assert re.get_representations() == volume_a_response['data']['volumes']
        re.representation = re.get_representations()[0]
        assert re.get_link() == volume_a_response['data']['volumes'][0]['link']['href']

        re1 = ResponseParser(volume_list_response, 'volumes')
        assert re1.response_key == 'data'
        assert re1.url_field == 'link'
        assert re1.get_representations() == volume_list_response['data']['volumes']
        re1.representation = re1.get_representations()[0]
        assert (
            re1.get_link() == volume_list_response['data']['volumes'][0]['link']['href']
        )

        re2 = ResponseParser(token_response_error)
        assert re2.get_status_body() == token_response_error['server']
        assert re2.get_error_code() == token_response_error['server']['code']
        assert re2.get_error_msg() == token_response_error['server']['message']
        assert re2.get_status() == token_response_error['server']['status']

    def test_requestParser(self):  # noqa: N802
        re = RequestParser(default_request['request']['params'])
        assert re.request_key == 'request'
        assert re.get_request_data() == default_request
