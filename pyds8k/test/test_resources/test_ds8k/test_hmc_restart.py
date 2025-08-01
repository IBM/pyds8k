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

from http import HTTPStatus

import responses
from responses import matchers

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_HMC, DS8K_HMC_RESTART

# from pyds8k.resources.ds8k.v1.hmc.restart import HMCRestart
from pyds8k.test.data import action_response, action_response_json
from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestHmcRestart(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()

    @responses.activate
    def test_hmc_restart(self):
        url = f'/{DS8K_HMC}/{DS8K_HMC_RESTART}'
        uri = f'{self.domain}{self.base_url}{url}'

        req = RequestParser({})
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )
        # Way 1
        resp1 = self.system.restart_hmc()

        assert responses.calls[-1].request.method == responses.POST
        assert resp1[0].status_code == HTTPStatus.CREATED
        assert resp1[1] == action_response['server']
