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

import httpretty

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_TSEREP
from pyds8k.resources.ds8k.v1.pools import Pool
from pyds8k.resources.ds8k.v1.tserep import TSERep
from pyds8k.test.data import (
    action_response_json,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

from .base import TestDS8KWithConnect

tserep_list_response_json = get_response_list_json_by_type(DS8K_TSEREP)


class TestTSERep(TestDS8KWithConnect):
    def test_pool_field(self):
        tserep = get_response_list_data_by_type(DS8K_TSEREP)['data'][DS8K_TSEREP][0]
        pool_id = tserep['pool'][Pool.id_field]
        tse = TSERep(self.client, info=tserep)
        self.assertEqual(tse.pool, pool_id)
        self.assertEqual(tse.representation['pool'], pool_id)
        self.assertIsInstance(tse._pool, Pool)
        self.assertEqual(tse._pool.id, pool_id)

    @httpretty.activate
    def test_update(self):
        pool_id = 'P1'
        url = f'/pools/{pool_id}/tserep'
        cap = '10'
        threshold = '70'
        httpretty.register_uri(
            httpretty.GET,
            self.domain + self.base_url + url,
            body=tserep_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK,
        )

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'cap': cap, 'threshold': threshold})
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (HTTPStatus.OK, headers, action_response_json)

        httpretty.register_uri(
            httpretty.PUT,
            self.domain + self.base_url + url,
            body=_verify_request,
            content_type='application/json',
        )
        tserep = self.system.get_tserep_by_pool(pool_id)

        tserep.cap = cap
        tserep.threshold = threshold
        tserep.save()
