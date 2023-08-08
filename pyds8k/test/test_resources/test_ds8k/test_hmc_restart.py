##############################################################################
# Copyright 2023 IBM Corp.
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
from pyds8k.resources.ds8k.v1.common.types import DS8K_HMC, DS8K_HMC_RESTART
# from pyds8k.resources.ds8k.v1.hmc.restart import HMCRestart
from pyds8k.test.data import action_response, action_response_json
from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestHmcRestart(TestDS8KWithConnect):

    def setUp(self):
        super(TestHmcRestart, self).setUp()

    @httpretty.activate
    def test_hmc_restart(self):
        url = '/{}/{}'.format(DS8K_HMC, DS8K_HMC_RESTART)

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            req = RequestParser({})
            assert {
                    **json.loads(request.body).get('request').get('params'),
                    **req.get_request_data().get('request').get('params')
                   } == json.loads(request.body).get('request').get('params')
            return (201, headers, action_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        # Way 1
        resp1 = self.system.restart_hmc()

        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertEqual(resp1[0].status_code, 201)
        self.assertEqual(resp1[1], action_response['server'])
